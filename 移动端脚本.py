# __init__.py 为初始化加载文件
# 导入系统资源模块
from ascript.android.system import R
# 导入动作模块
from ascript.android import action
# 导入节点检索模块
from ascript.android import node
# 导入图色检索模块
from ascript.android import screen
from ascript.android.screen import Colors
from ascript.android.screen import FindColors
import time
from airscript.screen import Screen
import requests
import json

yolo识别服务url= "http://192.168.1.9:22234/recognize"

def 图色找血条位置():
    point=FindColors.find("959,240,#FF4177-#000101")
    if point:
        x=point.x
        y=point.y
        recty=y-20
        rectx=x-29
        rectx1=x+200
        recty1=y+200
        return [rectx,recty,rectx1,recty1]
    else:
        return None
def 远程调用yolo识别血条的怪():
    血条位置=图色找血条位置()
    if 血条位置:
        print('出现血条了')
        x,y,x1,y1=血条位置
        bp = Screen.bitmap(x,y,x1,y1)
        b64str = Screen.base64(bp)
        payload = json.dumps({'image': b64str})
        response = requests.post(yolo识别服务url, json=payload)
        # print(response.text)
        try:
            类别名字 = json.loads(response.text)['result'][0]['cls']
            概率 = json.loads(response.text)['result'][0]['conf']
            if float(概率)>0.4:
                print(类别名字, 概率)
                print('识别到了')
                # 识别到了
                return True
            else:
                print('没有爆爆狐但是概率:',概率)
                点击发起战斗()
                time.sleep(20)
                print('战斗结束', '20秒等待完毕！')
        except:
            print('没有爆爆狐')
            点击发起战斗()
            time.sleep(20)
            print('战斗结束','20秒等待完毕！')
    else:
        print('没找到血条')


def 点击发起战斗():
    action.click(x=1339, y=973)

def 传整个图片到服务器上():
    response = requests.post(yolo识别服务url)
    
    return
    bp = screen.capture()
    b64str = Screen.base64(bp)
    payload = json.dumps({'image': b64str})
    response = requests.post(yolo识别服务url, json=payload)
    # print(response.text)


传整个图片到服务器上()
exit()
while True:
    try:
        if 远程调用yolo识别血条的怪():
            break
        time.sleep(2)
    except:pass



