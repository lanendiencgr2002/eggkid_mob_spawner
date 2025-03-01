# eggkid_mob_spawner
 蛋仔大派对自动刷艾比脚本
 内容：
用airscript来进行手机自动化，用于执行手机游戏蛋仔大派对刷怪物的脚本，情况如下首先手机会运行脚本，走到指定位置等待怪物，然后怪物如果在就截图发给电脑端部署的flask应用，两者进行http通信，手机端会把截图转化为base64编码发送给服务端，服务端会返回怪物是哪个类别的，这样来进行怪物的识别，然后手机端将会一直击败怪物，怪物会一直刷新，直到刷出想要的那个类别

简要使用步骤
1. 启动检测服务器flask
2. 启动刷怪脚本

# 标注步骤
1. 将图片放datasets\bvn\images\train下
2. 建立好classes.txt文件在datasets\bvn\labels\train下
3. 运行auto_labeltool\labelimg_autotool改版2.py
4. 点击open dir，选择datasets\bvn\images\train 还有change dir选择datasets\bvn\labels\train
5. 开始标注

# 训练步骤
1. 将图片放datasets\bvn\images\train
2. 进行标注
3. 更改data.yaml
4. 更改trainyolo.py的pt路径 还有data.yaml的路径
5. 运行trainyolo.py

# 说明
在yolo_worker中的老的模型训练
trian6是我重新训练的模型，也就是将游戏场景固定下来，每次到指定位置，然后是4个类别，大概是分辨率200*200  每个类别30个图片训练来的

train7同上，每个类别新增了25个图片

总共是120+100个图片
