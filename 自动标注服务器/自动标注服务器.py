import base64
import json

import cv2
from ultralytics import YOLO
import numpy as np
from flask import Flask, request, jsonify
import os

def 切换到脚本所在目录():
    # 获取当前脚本的绝对路径
    current_path = os.path.abspath(__file__)
    # 获取脚本所在目录
    script_dir = os.path.dirname(current_path)
    # 切换到脚本所在目录
    os.chdir(script_dir)
    print('当前目录切换成功',script_dir)

切换到脚本所在目录()

pt=r'D:\gitcangku\eggkid_mob_spawner\pt\baobaohu_newestpt\best.pt'

app = Flask(__name__)
class Model:
    def __init__(self, model_path=pt):
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
model = Model(pt)

@app.route('/recognize', methods=['POST'])
def recognize():
    if not request.json or 'image' not in request.json:
        return jsonify({'error': 'No image data provided'}), 400
        # 获取 base64 编码的图像数据
    image_base64 = json.loads(request.json)['image']
    print("接收到了image这个数据", image_base64)
    # 将 base64 编码的图像数据解码为字节数组
    image_bytes = base64.b64decode(image_base64)
    # 将字节数组转换为 NumPy 数组
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    # 使用 cv2.imdecode() 将 NumPy 数组解码为 cv2 对象
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    # 使用转换后的 cv2 对象进行检测
    result = model.detect(image)
    return jsonify({'result': result})

@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(port=22234)  # 在调试模式下运行，方便调试
    
