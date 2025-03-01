
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

def remove_duplicates(input_file, output_file):
    """
    对文本文件内容进行去重处理
    
    Args:
        input_file (str): 输入文件路径
        output_file (str): 输出文件路径
    """
    # 使用 set 存储不重复的行
    unique_lines = set()
    
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            # 去除行尾换行符并添加到集合中
            unique_lines.add(line.strip())
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in unique_lines:
            f.write(line + '\n')

if __name__ == '__main__':
    # 使用示例
    input_file = '论文题名和摘要.txt'  # 输入文件名
    output_file = '论文题名和摘要_去重.txt'  # 输出文件名
    
    remove_duplicates(input_file, output_file)
    print(f'去重完成! 结果已保存到 {output_file}') 