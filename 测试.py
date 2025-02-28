a = [1, 2, 3, 4]
b = [1, 2]

# 转换为集合
set_a = set(a)
set_b = set(b)

# 方法1: 使用 issubset() 方法
if set_b.issubset(set_a):
    print('在')
else:
    print('不在')

# 方法2: 使用 <= 运算符
if set_b <= set_a:
    print('在')
else:
    print('不在')

# 方法3: 检查交集长度
if len(set_b & set_a) == len(set_b):
    print('在')
else:
    print('不在')