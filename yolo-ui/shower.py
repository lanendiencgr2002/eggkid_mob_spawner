import shutil

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog, QMessageBox
import os
import 删除闪退文件
import trainyolo
import 图片缩短
import os

# 获取当前脚本的绝对路径
current_path = os.path.abspath(__file__)
# 获取脚本所在目录
script_dir = os.path.dirname(current_path)
# 切换到脚本所在目录
os.chdir(script_dir)
print('当前目录切换成功',script_dir)

class Stats:
    def __init__(self):
        self.ui = QUiLoader().load('./ui/e.ui')
        # 清除所有训练集验证集
        self.ui.pushButton.clicked.connect(self.pushButton)
        # 清除所有训练集
        self.ui.pushButton_2.clicked.connect(self.pushButton_2)
        # 开始训练
        self.ui.pushButton_3.clicked.connect(self.pushButton_3)
        # 删除runs
        self.ui.pushButton_4.clicked.connect(self.pushButton_4)
        # 解决闪退
        self.ui.pushButton_6.clicked.connect(self.pushButton_6)
        # 图缩短2倍
        self.ui.pushButton_5.clicked.connect(self.pushButton_5)

    # 图缩短2倍
    def pushButton_5(self):
        图片缩短.缩短2倍()

    # 解决闪退
    def pushButton_6(self):
        删除闪退文件.删除文件()

    # 删除runs
    def pushButton_4(self):
        文件夹="runs"
        if os.path.exists(文件夹):
            shutil.rmtree(文件夹)
            print(f"已删除{文件夹}")
        else:
            print(f"{文件夹}不在")

    # 开始训练
    def pushButton_3(self):
        datayaml=self.ui.textEdit_2.toPlainText().strip()
        pt=self.ui.textEdit.toPlainText().strip()
        trainyolo.开始训练(datayaml,pt)


    def 清除文件夹下所有文件(self, 文件夹):
        """清除指定文件夹下的所有文件"""
        for 文件 in os.listdir(文件夹):
            文件路径 = os.path.join(文件夹, 文件)
            try:
                if os.path.isfile(文件路径) or os.path.islink(文件路径):
                    os.unlink(文件路径)  # 删除文件或链接
                elif os.path.isdir(文件路径):
                    os.rmdir(文件路径)  # 删除空文件夹
            except Exception as e:
                print(f'清除 {文件路径} 失败. 原因: {e}')

    def delete_files_in_folder(self,folder_path):
        # 遍历文件夹中的所有项目
        for root, dirs, files in os.walk(folder_path):
            # 删除所有文件
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
    def pushButton(self):
        """清除所有训练集和验证集文件"""
        文件夹1 = "datasets/bvn/images/train"
        文件夹2 = "datasets/bvn/images/val"
        文件夹3 = "datasets/bvn/labels/train"
        文件夹4 = "datasets/bvn/labels/val"
        self.清除文件夹下所有文件(文件夹1)
        self.清除文件夹下所有文件(文件夹2)
        self.清除文件夹下所有文件(文件夹3)
        self.清除文件夹下所有文件(文件夹4)
        文件夹5="datasets/bvn/labels"
        self.delete_files_in_folder(文件夹5)

        print("所有训练集和验证集文件已清除。")
    def pushButton_2(self):
        """清除所有训练集文件"""
        文件夹1 = "datasets/bvn/images/train"
        文件夹3 = "datasets/bvn/labels/train"
        self.清除文件夹下所有文件(文件夹1)
        self.清除文件夹下所有文件(文件夹3)
        文件夹5 = "datasets/bvn/labels"
        self.delete_files_in_folder(文件夹5)
        print("所有训练集文件已清除。")


if __name__ == "__main__":
    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    app.exec_()