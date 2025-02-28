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
from ascript.android.screen.gp import GPStack
import cv2
from ascript.android.system import R
from ascript.android import plug
from ascript.android.screen import Ocr
from threading import Thread

yolo识别服务url="http://192.168.1.9:22234/recognize"

class 数据收集:
    def __init__(self):
        self.场景 = 2
        self.重试次数 = 3
        self.识别服务器url = "http://192.168.1.9:22234/recognize"
        self.截图次数=15
        self.截图间隔时间=5
        self.怪物刷新时间=60
        self.怪物死亡后消失时间=10
        self.检测战斗结束间隔时间=5
        self.击杀时间=20
        self.场景结束倒计时=300
        self.场景总共时间=1000
        self.击杀次数=5

    def 开始收集(self):
        """主循环,执行状态机流程"""
        while True:
            try:
                # 复位并走到指定位置
                是否找到血条 = 走到指定位置且得有血条(self.场景, self.重试次数)
                if not 是否找到血条:
                    print('没找到血条,重新复位来过')
                    continue
                # 击杀结束后等待怪物刷新
                for _ in range(self.击杀次数):
                    print('检查是否存在血条，如果没有则重新等待')
                    if 图色找血条位置():
                        print('怪物刷新了,截图然后发起战斗')
                        是否成功截图一次=截图上传服务器(self.截图次数,self.截图间隔时间,self.识别服务器url)
                        if not 是否成功截图一次:
                            print('截图上传失败,重新进入场景')
                            重新进入场景()
                            break
                        # 但是发起战斗就是结束了
                        召唤艾比()
                        time.sleep(1)
                        # 这里发起战斗可能距离不够
                        点击发起战斗()
                        print('等待击杀时间')
                        time.sleep(self.击杀时间)
                        print('等待怪物死亡后消失时间')
                        time.sleep(self.怪物死亡后消失时间)
                        收回艾比()
                        print('等待怪物刷新时间')
                        time.sleep(self.怪物刷新时间)
                    else:
                        print('没找到血条,重新复位来过')
                        time.sleep(10)
                        continue
                重新进入场景()
                # 进入到下次循环
                continue
            except Exception as e:
                print(f'发生异常: {e}')
                # 发生异常时重新进入场景
                重新进入场景()
                continue
def 图色找血条位置():
    '''
    如果是推荐召唤那么不是血条
    如果超出了范围，则返回None
    '''
    # 推荐召唤范围为[1333,842,1517,945])
    try:
        # 从左上开始往右下
        point=FindColors.find("0,0,#FF4177")
        # 推荐召唤的红色点不算血条
        if 1333<point.x<1517 and 842<point.y<945:
            return None
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
    except:
        print('图色找血条位置失败,默认返回None')
        return None
def 远程调用yolo识别血条的怪():
    血条位置=图色找血条位置()
    if 血条位置:
        print('出现血条了')
        x,y,x1,y1=血条位置
        try:
            bp = Screen.bitmap(x,y,x1,y1)
            b64str = Screen.base64(bp)
            payload = json.dumps({'image': b64str})
            response = requests.post(yolo识别服务url, json=payload)
        except:
            print('远程调用yolo识别血条的怪失败')
            return False
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
def 点击取消战斗():
    '''
    发起战斗时，再次发起战斗就是取消战斗
    '''
    raise NotImplementedError
    return 
def 传整个图片到服务器上():
    b64_str = screen.bitmap_base64()
    payload = json.dumps({'image': b64_str})
    response = requests.post(yolo识别服务url, json=payload)
    # print(response.text)
def 收回艾比():
    i=5
    while i>0:
        action.click(x=249, y=245)
        time.sleep(.4)
        i-=1
def 召唤艾比():
    i=5
    while i>0:
        action.click(x=1410, y=831)
        time.sleep(1)
        i-=1
def 复位():
    action.click(x=179, y=106)
    time.sleep(.2)
    action.click(x=179, y=106)
def 转固定视角():
    action.slide(x=1276,y=444,x1=950,y1=444,dur=1000)
def 转固定视角2():
    action.slide(x=1314,y=413,x1=1544,y1=413,dur=2000)
def 直走x秒(x秒):
    action.Touch.down(x=300,y=816,dur=20)
    action.Touch.move(x=300,y=607,dur=20)
    time.sleep(x秒)
    action.Touch.up(x=300,y=607,dur=20)
def 斜着走x秒(x秒):
    action.Touch.down(x=300,y=816,dur=20)
    action.Touch.move(x=360,y=628,dur=20)
    time.sleep(x秒)
    action.Touch.up(x=360,y=628,dur=20)
def 检查是否返回():
    def gp(cv_img=None):
        #检查是否存在文字
        gp_stack = GPStack(cv_img)
        gp_stack.add(Ocr(mode= Ocr.MODE_MLK,rect =[1613,940,1830,1029]))
        gp_result = gp_stack.run()
        return gp_result
        # 如需运行,取消以下代码注释
        # res = gp()
        # print(res.data)
    res = gp()
    if res.data:
        print('存在文字')
        if '返回' in res.data:
            return True
        else:
            return False
    else:
        print('不存在文字')
        return False
def 点击返回():
    action.click(x=1697,y=988)
def 复位且到指定位置():
    复位且收回艾比()
    转固定视角()
    直走x秒(10)
    斜着走x秒(5)
def 复位且到指定位置2():
    复位且收回艾比()
    转固定视角2()
    # 15秒是对的
    直走x秒(15.5)
def 走到指定位置且得有血条(场景,重试次数=3):
    '''
    走到指定位置且得有血条，重试3次，如果没血条，会自动回收艾比
    参数：
    场景：
    1. 第一场景
    2. 第二场景
    返回值:
    成功返回True
    失败返回False
    '''
    i=0
    while i<重试次数:
        try:
            if 场景==1:
                print('走到指定位置1')
                复位且到指定位置()
                print('走到指定位置1成功')
            elif 场景==2:
                print('走到指定位置2')
                复位且到指定位置2()
                print('走到指定位置2成功')
        except Exception as e:
            print('走到指定位置失败',e)
            i+=1
            continue
        if 图色找血条位置():
            print('走到指定位置看且有血条')
            return True
        else:
            print('走到指定位置，但没血条，正在重试')
            i+=1
    print('走到指定位置看且没血条')
    return False
def 血条位置截图传到服务器上(yolo识别服务url):
    '''
    传血条位置截图到服务器上
    成功返回True
    失败返回False
    '''
    血条位置=图色找血条位置()
    if 血条位置:
        print('出现血条了')
        try:
            x,y,x1,y1=血条位置
            bp = Screen.bitmap(x,y,x1,y1)
            b64str = Screen.base64(bp)
            payload = json.dumps({'image': b64str})
            response = requests.post(yolo识别服务url, json=payload)
            print(response.text)
            return True
        except Exception as e:
            print('截图传到服务器上失败',e)
            return False
    else:
        print('没找到血条')
        return False
def 复位且收回艾比():
    复位()
    time.sleep(.5)
    收回艾比()
def 判断是否倒计时():
    try:
        白色点个数=Colors.count("#FFFFFF",rect=[876,162,1060,232])
        if 白色点个数>1000:
            return True
        else:
            return False
    except Exception as e:
        print('判断是否倒计时失败',e)
        return False
def 重新进入场景():
    try:
        # 左箭头
        action.click(x=84,y=107)
        time.sleep(1)
        # 退出游戏
        action.click(x=1532,y=884)
        time.sleep(1)
        # 确认
        action.click(x=1674,y=639)
        time.sleep(3)
        # 返回
        action.click(x=1701,y=968)
        time.sleep(30)
        # 选择地图
        action.click(x=1180,y=287)
        time.sleep(5)
        # 点击前往
        action.click(x=1567,y=968)
        time.sleep(20)
        print('重新进入场景成功')
    except Exception as e:
        print('重新进入场景失败',e)
def 临时收集爆爆狐在():
    while True:
        是否传成功 = 血条位置截图传到服务器上(yolo识别服务url)
        if not 是否传成功:
            print('截图传输失败,重试')
            time.sleep(10)
            continue
        是否成功截图一次=True
        time.sleep(10)
def 截图上传服务器(截图次数,截图间隔时间,识别服务器url):
    '''
    参数：
    截图次数：int
    截图间隔时间：int
    识别服务器url：str
    返回值：
    是否成功截图一次：bool
    '''
    是否成功截图一次=False
    while 截图次数>0:
        截图次数-=1
        # 找到血条,截图传服务器
        是否传成功 = 血条位置截图传到服务器上(识别服务器url)
        if not 是否传成功:
            print('截图传输失败,重试')
            time.sleep(截图间隔时间)
            continue
        是否成功截图一次=True
        time.sleep(截图间隔时间)
    return 是否成功截图一次
def 到达场景后的测试():
    while True:
        print('检查是否存在血条，如果没有则重新等待')
        if 图色找血条位置():
            print('怪物刷新了,截图然后发起战斗')
            是否成功截图一次=截图上传服务器(5,5,yolo识别服务url)
            if not 是否成功截图一次:
                print('截图上传失败,重新进入场景')
                重新进入场景()
                break
            # 但是发起战斗就是结束了
            召唤艾比()
            time.sleep(1)
            点击发起战斗()
            time.sleep(20)
            收回艾比()
            time.sleep(50)
print('开始')
# 传整个图片到服务器上()
# 收回艾比()
# 召唤艾比()
# 复位且到指定位置()
# 临时收集爆爆狐在()
# 走到指定位置且得有血条(场景=2)
# 重新进入场景()
# 血条位置截图传到服务器上(yolo识别服务url)
收集器 = 数据收集()
收集器.开始收集()
# 到达场景后的测试()  
print('结束')