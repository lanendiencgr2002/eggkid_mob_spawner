import os

# file_path = r"C:\Users\11923\.labelImgSettings.pkl"
file_path = os.path.join(os.path.expanduser('~'), '.labelImgSettings.pkl')

def 删除闪退文件():
    if os.path.exists(file_path):
        os.remove(file_path)
        print("文件已删除")
    else:
        print("文件不存在")

if __name__ == '__main__':
    删除闪退文件()
