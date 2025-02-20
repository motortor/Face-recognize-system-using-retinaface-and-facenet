import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体

# 读取数据文件
data = pd.read_csv('jilu.txt', sep='  ', engine='python', names=['name', 'time', 'status'])

# 提取时间信息，生成新的列
data['hour'] = pd.to_datetime(data['time']).dt.hour

# 按小时统计每个时间段返回的次数
hourly_count = data[data['status'].isin(['准时', '晚归'])].groupby('hour')['time'].nunique()

# 新建一个全零的Series，将hourly_count中的数据加入进去
all_hours = pd.Series(0, index=range(24))
all_hours[hourly_count.index] = hourly_count.values

# 绘制折线图
plt.plot(np.array(all_hours.index), all_hours.values, marker='o', markersize=6, linewidth=2)
plt.xticks(np.arange(24))

# 添加0值的折点
for i in range(24):
    if all_hours[i] == 0:
        plt.plot(i, 0, marker='o', markersize=6, color='gray')

# 设置图表属性
plt.title('24小时内学生返回宿舍频率变化情况')
plt.xlabel('时间')
plt.ylabel('次数')
plt.xticks(range(24))
plt.legend(['返回宿舍频率'])

# 显示图表
plt.show()
