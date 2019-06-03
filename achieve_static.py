import hashlib
import random
import matplotlib.pyplot as plt
import scipy.stats as stats

# 数据无动态加载的情况
# 机器名称
machine_name = ['redis01', 'redis02', 'mysql01', 'mysql02']
node_list = []

# 节点名称
for name in machine_name:
    for i in range(100):
        node_name = name+'-'+str(i)
        node_list.append(node_name)

hash_list = []
record_dict = {}

# 各个节点的hash, 对hash取模
for node in node_list:
    h_node = int(hashlib.md5(node.encode(encoding='utf-8')).hexdigest(), 16)
    # record_dict[str(h_node)] = node
    h_mode = h_node%2**64
    hash_list.append(h_node%2**64)
    record_dict[str(h_mode)] = node

hash_list.sort()
tmp = []
for h in hash_list:
    tmp_dict = {str(h): []}
    tmp.append(tmp_dict)

print('recored', record_dict)
print('tmp', tmp)

# 数据打在hash环上
data_list = [str(random.randint(1, 100000)) for i in range(1, 1001)]

for data in data_list:
    data_h = int(hashlib.md5(data.encode(encoding='utf-8')).hexdigest(), 16)%2**64
    # 遍历法寻找位置
    tmp_h = hash_list.copy()
    tmp_h.append(data_h)
    tmp_h.sort()
    index = tmp_h.index(data_h)
    if index == len(tmp_h)-1:
        # 到开头
        for key, value in tmp[0].items():
            value.append(data_h)
    else:
        for key, value in tmp[index].items():
            value.append(data_h)
    del(tmp_h)
    # TODO 红黑树的方法寻找位置
print(tmp)

# 统计数据
test_data = []
source_data = {}
for data in tmp:
    for k, v in data.items():
        name = record_dict[k]
        test_data.append(len(v))
        source_data[name] = len(v)

plt.figure(figsize=(40, 10))
for a, b in source_data.items():
    plt.text(a, b+0.05, '%.0f'%b, ha='center', va='bottom', fontsize=11)

# 设置x轴y轴
x_axis = tuple(source_data.keys())
y_axis = tuple(source_data.values())

plt.bar(x_axis, y_axis, color='rgb')

plt.ylim(0, 300)
plt.show()

print('===============================')
# 夏皮罗威尔克检测,小样本数据
w = stats.shapiro(test_data)
print(w)

# TODO 动态加载机器或数据,可最近匹配机器,而不用重新计算机器的hash值
