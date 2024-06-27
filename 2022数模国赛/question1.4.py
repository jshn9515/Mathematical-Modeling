import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import scipy.stats as stats

np.set_printoptions(4, suppress=True)
plt.rcParams['font.sans-serif'] = ['DengXian']
plt.rcParams['font.size'] = 15
df1 = pd.read_excel('问题1-铅钡高钾组合数据.xlsx', sheet_name='铅钡-风化', usecols='C:J')  # noqa
df2 = pd.read_excel('问题1-铅钡高钾组合数据.xlsx', sheet_name='铅钡-未风化', usecols='C:J')  # noqa
pd1 = stats.norm.fit(df1.iloc[:, 0])
pd2 = stats.norm.fit(df2.iloc[:, 0])
x1 = np.arange(np.floor(df1.iloc[:, 0].min()), np.ceil(df1.iloc[:, 0].max()), 0.1)
x2 = np.arange(np.floor(df2.iloc[:, 0].min()), np.ceil(df2.iloc[:, 0].max()), 0.1)
y1 = stats.norm.pdf(x1, loc=pd1[0], scale=pd1[1])
y2 = stats.norm.pdf(x2, loc=pd2[0], scale=pd2[1])
x3 = 18
y3 = stats.norm.pdf(x3, loc=pd1[0], scale=pd1[1])
x4 = x3 + pd2[0] - pd1[0]
y4 = stats.norm.pdf(x4, loc=pd2[0], scale=pd2[1])

plt.figure(1)
plt.plot(x1, y1, x2, y2)
plt.plot(x3, y3, 'black', x4, y4, 'black', marker='.', markersize=10)
plt.text(x3 - 2, y3, r'$\it{x}$', fontsize=18)
plt.text(x4 + 1, y4, r'$\it{y}$', fontsize=18)
style = patches.ArrowStyle('->', head_length=1.2, head_width=0.8)
plt.annotate('', xy=(x4 - 2, y4), xytext=(x3 + 2, y3), arrowprops=dict(arrowstyle=style, linewidth=1.5))
plt.legend(['SiO2风化', 'SiO2未风化'], loc='upper right')
plt.title('SiO2-铅钡-风化与未风化概率密度对比图')

predict = np.zeros(df1.shape)
for i in range(df1.shape[1]):
    pd1 = stats.norm.fit(df1.iloc[:, i])
    pd2 = stats.norm.fit(df2.iloc[:, i])
    predict[:, i] = (df1.iloc[:, i] - pd1[0]) / pd1[1] * pd2[1] + pd2[0]
predict[predict < 0] = 0
predict = predict / np.sum(predict, axis=1, keepdims=True) * 100
predict = pd.DataFrame(predict, index=df1.index, columns=df1.columns)
# predict.to_excel('铅钡风化还原数据.xlsx', index_label='文物编号')
plt.show()
