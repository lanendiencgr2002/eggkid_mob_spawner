from ultralytics import YOLO

def main():
    model = YOLO('last.pt')
    model.train(data='data.yaml', workers=1, epochs=50, batch=4)

if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()
    main()