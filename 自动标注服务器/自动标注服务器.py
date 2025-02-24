import base64
import json
import cv2
from ultralytics import YOLO
import numpy as np
from flask import Flask, request, jsonify
import os
from datetime import datetime
# 获取当前脚本的绝对路径
current_path = os.path.abspath(__file__)
# 获取脚本所在目录
script_dir = os.path.dirname(current_path)
# 切换到脚本所在目录
os.chdir(script_dir)
print('当前目录切换成功',script_dir)

class Config:
    # 默认配置
    接收截图 = True
    
    @classmethod
    def load(cls, config_path='./cofig.json'):
        """加载配置文件到类属性"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
                # 将配置项设置为类属性
                for key, value in config_dict.items():
                    setattr(cls, key, value)
        except Exception as e:
            print(f"加载配置失败,使用默认配置: {e}")

# 初始化时加载配置
Config.load()

app = Flask(__name__)
class Model:
    def __init__(self, model_path="./yolov8n.pt"):
        self.model = YOLO(model_path)
    def detect(self, img_path):
        results = self.model(img_path)
        names = self.model.names
        cls = results[0].boxes.cls.cpu().numpy().astype(np.int32)
        obj_names = [names[i] for i in cls]
        xyxy = results[0].boxes.xyxy.cpu().numpy().astype(np.int32).tolist()
        conf = results[0].boxes.conf.cpu().numpy().tolist()
        objs = [
            {
                'cls': obj_names[id_],
                'xyxy': xyxy[id_],
                'conf': conf[id_]
            } for id_ in range(len(obj_names))
        ]
        return objs
# model = Model('./last.pt')

@app.route('/recognize', methods=['POST'])
def recognize():
    print("有请求过来了")
    if not request.json or 'image' not in request.json:
        return jsonify({'error': 'No image data provided'}), 400
    
    image_base64 = json.loads(request.json)['image']
    image_bytes = base64.b64decode(image_base64)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    
    if Config.接收截图:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        cv2.imwrite(f'./服务器接收的截图/{timestamp}.png', image)

    return jsonify({'message': '图片已保存'})
    # 检测
    result = model.detect(image)
    # 类别名字
    name= result[0]['cls']
    # 概率
    conf= result[0]['conf']
    # 返回结果
    return jsonify({'name': name,'conf':conf})

@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=22234)  # 在调试模式下运行，方便调试
    
