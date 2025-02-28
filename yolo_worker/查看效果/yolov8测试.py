# 导入YOLO模块和相关库
import time

import cv2
from matplotlib import pyplot as plt
from ultralytics import YOLO

yolo = YOLO("../best.pt", task="detect")
result = yolo(source='img_5.png',show=True)
print(result[0].boxes)
cv2.waitKey(0)
# print(result)