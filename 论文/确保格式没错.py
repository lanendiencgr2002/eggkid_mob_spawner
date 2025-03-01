import os
def 切换到脚本所在目录():
    # 获取当前脚本的绝对路径
    current_path = os.path.abspath(__file__)
    # 获取脚本所在目录
    script_dir = os.path.dirname(current_path)
    # 切换到脚本所在目录
    os.chdir(script_dir)
    print('当前目录切换成功',script_dir)
切换到脚本所在目录()


论文txt='论文题名和摘要.txt'

def 确保格式没错():
    min=100
    with open(论文txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        index=lines.index(line)
        if index%2==1:
            print(index,line)
            max=len(line)
    print(max)

if __name__ == '__main__':
    确保格式没错()

