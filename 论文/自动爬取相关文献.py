from DrissionPage import ChromiumPage, ChromiumOptions
import os
import time
def dp配置():
    co = ChromiumOptions().set_local_port(8077)
    co.set_timeouts(base=5)
    page = ChromiumPage(addr_or_opts=co)
    print(f"浏览器启动端口: {page.address}")
    return page
def 切换到脚本所在目录():
    # 获取当前脚本的绝对路径
    current_path = os.path.abspath(__file__)
    # 获取脚本所在目录
    script_dir = os.path.dirname(current_path)
    # 切换到脚本所在目录
    os.chdir(script_dir)
    print('当前目录切换成功',script_dir)
切换到脚本所在目录()
import dp标签页
page=dp配置()

def 获取当前页所有论文题名和摘要():
    结果=[]
    tab=dp标签页.根据标题取当前tab(page,'中国知网')
    题名s=tab.eles('.fz14')
    for 题名 in 题名s:
        print(f'当前页第{题名s.index(题名)+1}个论文题名，{题名.text}')
        题名.click()
        摘要=dp标签页.返回最新tab(page).ele('#ChDivSummary').text
        追加到文件(f'{题名.text}\n{摘要}')
        dp标签页.返回最新tab(page).close()
        结果.append(f'{题名.text}\n{摘要}')
    return 结果
def 获取摘要():
    tab=dp标签页.根据标题取当前tab(page,'中国知网')
    摘要=tab.ele('#ChDivSummary').text
    print(摘要)

def 追加到文件(内容):
    with open('论文题名和摘要.txt','a',encoding='utf-8') as f:
        f.write(内容+'\n')

def 不断获取论文题名和摘要写到记事本中():
    while True:
        结果=获取当前页所有论文题名和摘要()
        PageNext=dp标签页.根据标题取当前tab(page,'中国知网')
        PageNext.ele('#PageNext').click()
        time.sleep(5)

if __name__ == "__main__":
    # yolov8 30页 按时间降序
    print(page.title)
    不断获取论文题名和摘要写到记事本中()
