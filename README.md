# eggkid_mob_spawner
 蛋仔大派对自动刷艾比脚本

# 简要使用步骤
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
