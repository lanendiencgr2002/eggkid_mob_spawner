import cv2
import os
import shutil

def 缩短2倍():
    # 设置输入和输出文件夹
    input_folder = 'datasets/bvn/images/train'
    output_folder = 'datasets/bvn/images/train'  # 输出文件夹与输入文件夹相同

    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的图片
    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            # 读取图片
            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path)

            # 缩小图片尺寸
            new_size = (img.shape[1] // 2, img.shape[0] // 2)
            resized_img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)

            # 保存缩小后的图片
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, resized_img)
            print(f'Resized {filename} and saved to {output_folder}')