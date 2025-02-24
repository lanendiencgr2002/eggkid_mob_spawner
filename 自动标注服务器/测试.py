import cv2
import numpy as np

def find_health_bar_region(image):
    # 定义颜色范围(BGR格式)
    lower = np.array([0, 1, 1])  # #000101
    upper = np.array([255, 65, 119])  # #FF4177
    
    # 创建感兴趣区域来限制搜索范围
    roi_x, roi_y = 900, 200  # 搜索中心点附近
    roi_w, roi_h = 120, 80   # 搜索区域大小
    roi = image[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
    
    # 查找颜色范围内的像素
    mask = cv2.inRange(roi, lower, upper)
    
    # 找到非零点位置
    points = cv2.findNonZero(mask)
    
    if points is not None:
        # 找到了匹配的颜色点
        # 取第一个点的位置(相对于ROI)
        x, y = points[0][0]
        
        # 转换回原图坐标
        x += roi_x
        y += roi_y
        
        # 计算矩形区域
        rect_x = x - 29
        rect_y = y - 20
        rect_x1 = x + 200
        rect_y1 = y + 200
        
        return [rect_x, rect_y, rect_x1, rect_y1]
    
    return None

if __name__ == '__main__':
    # 读取图片
    image = cv2.imread('D:\gitcangku\eggkid_mob_spawner\yolo-ui\服务器识别图片\image_1721628555.jpg')
    # 查找血条区域
    health_bar_region = find_health_bar_region(image)
    print(health_bar_region)

