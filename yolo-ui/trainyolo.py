from ultralytics import YOLO

def main():
    model = YOLO('yolov8n.pt')
    model.train(data='data.yaml', workers=1, epochs=30, batch=8)

def 开始训练(datayaml="data.yaml",pt='best.pt'):
    from multiprocessing import freeze_support
    freeze_support()
    model = YOLO(pt)
    model.train(data=datayaml, workers=1, epochs=30, batch=16)

if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()
    main()

