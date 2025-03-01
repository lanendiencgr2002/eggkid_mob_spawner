import time
from DrissionPage.common import Actions
from DrissionPage import ChromiumPage, ChromiumOptions

def dp配置():
    co = ChromiumOptions().set_local_port(8077)
    co.set_timeouts(base=5)
    page = ChromiumPage(addr_or_opts=co)
    print(f"浏览器启动端口: {page.address}")
    return page


def 根据标题取当前tab(ele,标题):
    """
    根据标题查找当前打开的标签页
    
    Args:
        ele: DrissionPage对象
        标题: 要查找的标签页标题 包含即可
        
    Returns:
        Tab对象: 如果找到匹配的标签页则返回该Tab对象
        None: 如果未找到匹配的标签页则返回None
    """
    tabs=ele.get_tabs()
    for tab in tabs:
        if 标题 in tab.title:
            return tab
    return None

def 根据url获取当前tab(ele,url):
    """
    根据URL查找当前打开的标签页
    
    Args:
        ele: DrissionPage对象 
        url: 要查找的标签页URL 包含即可
        
    Returns:
        Tab对象: 如果找到匹配的标签页则返回该Tab对象
        None: 如果未找到匹配的标签页则返回None
    """
    tabs=ele.get_tabs()
    for tab in tabs:
        if url in tab.url:
            return tab
    return None

def 返回最新tab(ele):
    return ele.latest_tab

def 测试():
    tab=返回最新tab(page)
    print(tab.title)

if __name__ == '__main__':
    page=dp配置()
    测试()  




