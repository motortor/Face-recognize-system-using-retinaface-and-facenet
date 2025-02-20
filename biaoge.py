import pandas as pd

# 读取文件
df = pd.read_csv('jilu.txt', sep='\s{2,}', engine='python', header=None, names=['姓名', '时间', '状态'])

# 提取每个学生的状态
df['状态'] = df['状态'].apply(lambda x: '准时次数' if x == '准时' else '晚归次数')

# 统计每个学生的次数
df_counts = df.groupby(['姓名', '状态']).count()
df_counts = df_counts.unstack(level=1, fill_value=0)['时间']
df_counts['总次数'] = df_counts.sum(axis=1)

# 输出到Excel表格
df_counts.to_excel('output.xlsx')
