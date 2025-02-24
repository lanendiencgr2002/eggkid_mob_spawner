import requests
import json

# 设置Flask服务的地址
url = 'http://localhost:22234/recognize'  # 根据实际情况更改地址和端口号

# 准备要发送的图片文件
files = {'image': r'C:\Users\11923\PycharmProjects\module_shared\yolov8\自动标注服务器\uploaded_image_2.png'}  # 替换为你的图片路径

# 发送POST请求
response = requests.post(url, json=json.dumps(files))

# 解析响应
if response.status_code == 200:
    result = response.json()['result']
    print("识别结果：", result)
else:
    print("请求失败：", response.status_code)