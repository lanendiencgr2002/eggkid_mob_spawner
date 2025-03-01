import json
import re
import requests
from collections import Counter
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def 切换到脚本所在目录():
    # 获取当前脚本的绝对路径
    current_path = os.path.abspath(__file__)
    # 获取脚本所在目录
    script_dir = os.path.dirname(current_path)
    # 切换到脚本所在目录
    os.chdir(script_dir)
    print('当前目录切换成功',script_dir)
切换到脚本所在目录()


# 项目详细描述
PROJECT_DESCRIPTION = """
项目名称: 基于YOLOv8n的自动刷怪系统

技术细节:
1. 深度学习模型: YOLOv8n
2. 部署方式: Flask Web服务
3. 训练数据:
   - 总计200张训练图片
   - 分两批训练(第一批100张左右,第二批剩余)
   - 每批训练约30次
   - 图像尺寸: 200*200像素

应用场景:
1. 游戏环境: 蛋仔大派对中艾比场景
2. 目标检测:
   - 血条识别
   - 血条右下200距离范围内的怪物识别
   - 4种怪物类型分类

自动化功能:
1. 实时识别当前怪物类型
2. 自动判断是否为目标怪物
3. 非目标怪物自动击杀
4. 等待刷新直到目标怪物出现
5. 目标怪物出现时停止操作

主要技术特点:
1. 实时目标检测
2. 小样本学习
3. Web服务部署
4. 游戏场景自动化
5. 特定区域目标识别
"""

# 定义关键词及其权重
keywords = {
    'yolo': 3,
    'yolov': 3,
    'detection': 2,
    'object detection': 3,
    'deep learning': 2,
    'flask': 2,
    'web': 1,
    'deploy': 2,
    'real-time': 2,
    'game': 2,
    'automation': 2,
    'small dataset': 2,
    'transfer learning': 2,
    'computer vision': 1,
    '目标检测': 3,
    '深度学习': 2,
    '部署': 2,
    '实时': 2,
    '游戏': 2,
    '自动化': 2,
    '小样本': 2,
    '迁移学习': 2
}

def get_ai_relevance(title, abstract):
    """使用AI接口计算文本相关度"""
    try:
        # 构造请求数据
        prompt = f"""
请作为论文专家,判断下面这篇论文与我的项目的相关度(0-100分)。

我的项目信息:
{PROJECT_DESCRIPTION}

待评估论文:
标题: {title}
摘要: {abstract}

请从以下几个方面评估相关度:
1. 技术相似度(使用的算法、模型、方法等)
2. 应用场景相似度(游戏、自动化、目标检测等)
3. 实现方式相似度(部署方式、数据处理等)
4. 创新点参考价值
5. 可借鉴内容的多少

请给出0-100的分数,100分表示完全相关且极具参考价值,0分表示完全不相关。
只需要返回分数即可,不需要解释。
"""
        
        data = {
            "问题": prompt
        }
        
        # 发送POST请求
        response = requests.post(
            'http://localhost:5000/chat',
            headers={
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                'Content-Type': 'application/json'
            },
            json=data,
            timeout=30  # 添加超时设置
        )
        
        # 检查响应状态
        response.raise_for_status()
        
        # 解析响应内容
        try:
            result = response.json()
            # print(f"DEBUG - API响应: {result}")  # 调试用
            
            # 处理嵌套的data结构
            if 'data' in result:
                data = result['data']
                if data['status'] == 'success':
                    score = float(data['message'])
                    return score
                else:
                    print(f"\nAPI返回非成功状态: {data}")
                    return 0
            else:
                print(f"\nAPI响应缺少data字段: {result}")
                return 0
                
        except json.JSONDecodeError as je:
            print(f"\nJSON解析错误: {je}")
            print(f"原始响应内容: {response.text}")
            return 0
        except KeyError as ke:
            print(f"\n响应格式错误: {ke}")
            print(f"响应内容: {result}")
            return 0
        except ValueError as ve:
            print(f"\n分数转换错误: {ve}")
            print(f"分数文本: {result.get('message')}")
            return 0
            
    except requests.RequestException as re:
        print(f"\n网络请求错误: {re}")
        return calculate_keyword_relevance(title + " " + abstract, keywords)
    except Exception as e:
        print(f"\n未预期的错误: {e}")
        print(f"错误类型: {type(e)}")
        return calculate_keyword_relevance(title + " " + abstract, keywords)

def calculate_keyword_relevance(text, keywords):
    """使用关键词匹配计算相关度(作为备选方案)"""
    score = 0
    text = text.lower()
    
    for keyword, weight in keywords.items():
        count = len(re.findall(keyword.lower(), text))
        score += count * weight
    
    # 将分数标准化到0-100
    max_possible_score = sum(weight * 5 for weight in keywords.values())  # 假设每个关键词最多出现5次
    score = min(100, score * 100 / max_possible_score)
    
    return score

def process_paper(args):
    """处理单篇论文的函数"""
    title, abstract = args
    try:
        score = get_ai_relevance(title, abstract)
        return (title, abstract, score)
    except Exception as e:
        print(f"\n处理论文出错: {e}")
        return (title, abstract, 0)

def filter_papers():
    # 读取论文数据
    with open('论文题名和摘要.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 准备论文数据
    papers = []
    for i in range(0, len(lines), 2):
        if i + 1 >= len(lines):
            break
        title = lines[i].strip()
        abstract = lines[i + 1].strip()
        if title and abstract:
            papers.append((title, abstract))
    
    # 使用线程池处理论文
    paper_scores = []
    max_workers = min(20, len(papers))  # 最多20个线程
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_paper = {executor.submit(process_paper, paper): paper for paper in papers}
        
        # 使用tqdm显示进度条
        with tqdm(total=len(papers), desc="处理论文") as pbar:
            for future in as_completed(future_to_paper):
                try:
                    result = future.result()
                    if result:
                        paper_scores.append(result)
                except Exception as e:
                    print(f"\n处理论文时发生错误: {e}")
                pbar.update(1)
    
    # 按分数降序排序
    paper_scores.sort(key=lambda x: x[2], reverse=True)
    
    # 返回前20篇最相关的论文
    return paper_scores[:20]

def save_results(relevant_papers):
    """保存结果到记事本"""
    # 生成文件名，包含时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'推荐论文_{timestamp}.txt'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("基于YOLOv8n的自动刷怪系统 - 相关论文推荐\n")
        f.write("=" * 50 + "\n\n")
        
        # 按分数降序排序
        sorted_papers = sorted(relevant_papers, key=lambda x: x[2], reverse=True)
        
        for i, (title, _, score) in enumerate(sorted_papers, 1):
            f.write(f"{score:.2f}分 - {title}\n")
    
    print(f"\n结果已保存到: {filename}")

def main():
    relevant_papers = filter_papers()
    
    print(f"\n找到{len(relevant_papers)}篇相关论文:")
    for i, (title, abstract, score) in enumerate(relevant_papers, 1):
        print(f"\n论文 {i} (相关度分数: {score:.2f}):")
        print(f"标题: {title}")
        print(f"摘要: {abstract}")
        print("-" * 80)
    
    # 保存结果到记事本
    save_results(relevant_papers)

if __name__ == "__main__":
    main()