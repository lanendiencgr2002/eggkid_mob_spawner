import base64
import json
import os

import cv2
import pygame
from ultralytics import YOLO
import numpy as np
from flask import Flask, request, jsonify
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

model = Model('best.pt')
def 播放mp3(mp3文件路径='e.wav'):
    # 转音频 https://www.aconvert.com/cn/audio/
    pygame.mixer.init()
    sound = pygame.mixer.Sound(mp3文件路径)
    channel = pygame.mixer.Channel(0)  # 获取第 0 通道
    channel.play(sound)
    # 使用 channel.get_busy() 来检查音频是否仍在播放
    while channel.get_busy():
        pass
    sound.stop()
    pygame.mixer.quit()
@app.route('/recognize', methods=['POST'])
def recognize():
    if not request.json or 'image' not in request.json:
        return jsonify({'error': 'No image data provided'}), 400
        # 获取 base64 编码的图像数据
    # print(request.json)
    # 播放mp3('aa.mp3')
    image_base64 = json.loads(request.json)['image']
    # print("接收到了image这个数据", image_base64)
    # 创建用于存储图片的文件夹
    folder_name = "服务器识别图片"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 将 base64 编码的图像数据解码为字节数组
    image_bytes = base64.b64decode(image_base64)

    # 生成唯一的文件名（这里使用时间戳）
    import time
    timestamp = int(time.time())
    file_name = f"image_{timestamp}.jpg"

    # 将图片保存到指定文件夹
    file_path = os.path.join(folder_name, file_name)
    with open(file_path, "wb") as f:
        f.write(image_bytes)

    print(f"图片已保存到: {file_path}")

    # 将字节数组转换为 NumPy 数组
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    # 使用 cv2.imdecode() 将 NumPy 数组解码为 cv2 对象
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    # 使用转换后的 cv2 对象进行检测
    result = model.detect(image)
    # 如果结果不为空，则返回结果
    if result:
        print(result)
        播放mp3('aa.mp3')
    else:
        print("没有检测到任何东西")
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(port=22234,host='0.0.0.0')  # 在调试模式下运行，方便调试
