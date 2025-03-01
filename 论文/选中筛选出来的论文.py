import os
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage import ChromiumOptions
import time
import dp标签页

def 切换到脚本所在目录():
    # 获取当前脚本的绝对路径
    current_path = os.path.abspath(__file__)
    # 获取脚本所在目录
    script_dir = os.path.dirname(current_path)
    # 切换到脚本所在目录
    os.chdir(script_dir)
    print('当前目录切换成功',script_dir)
切换到脚本所在目录()

def dp配置():
    co = ChromiumOptions().set_local_port(8077)
    co.set_timeouts(base=5)
    page = ChromiumPage(addr_or_opts=co)
    print(f"浏览器启动端口: {page.address}")
    return page
page=dp配置()

def 读取所有论文标题():
    """从推荐论文文件中读取论文标题"""
    论文题目 = []
    try:
        with open(推荐论文目录, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                # 跳过标题、分隔线和空行
                if '=' in line or '基于YOLOv8n' in line or not line.strip():
                    continue
                # 提取论文标题
                if '分 - ' in line:
                    分数, 标题 = line.strip().split('分 - ')
                    分数 = float(分数)
                    # 论文题目.append({
                    #     '分数': 分数,
                    #     '标题': 标题
                    # })
                    论文题目.append(标题)
        
        # 打印读取结果
        # for i, 论文 in enumerate(论文题目, 1):
        #     print(f"{i}. {论文['分数']}分 - {论文['标题']}")
            
    except Exception as e:
        print(f"读取论文标题时出错: {e}")
    
    return 论文题目

def 选中所有论文():
    论文标题=读取所有论文标题()
    for 论文标题 in 论文标题:
        tab=dp标签页.根据标题取当前tab(page,'中国知网')
        搜索栏=tab.ele('#txt_search')
        搜索栏.clear()
        搜索栏.input(论文标题+'\n')
        time.sleep(1)
        选中(tab,论文标题)

def 选中(tab,论文标题):
    所有题名=tab.eles('.name')
    所有点选框=tab.eles('.cbItem')
    if len(所有题名)==0:
        print('没有找到论文,论文题目为',论文标题)
        return
    for 题名 in 所有题名:
        # print(论文标题,题名.text)
        if 论文标题[:len(论文标题)] in 题名.text:
            # print('找到了')
            点选框=所有点选框[所有题名.index(题名)]
            点选框.click()
            return
    print('没有找到论文,论文题目为',论文标题)
    return
    

推荐论文目录=r'推荐论文_20250301_141101.txt'


if __name__=='__main__':
    # print(读取所有论文标题())
    选中所有论文()
    # print(page.ele('.name').text)