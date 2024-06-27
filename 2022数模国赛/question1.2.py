import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

plt.rcParams['font.sans-serif'] = ['DengXian']
plt.rcParams['font.size'] = 15
plt.rcParams['axes.unicode_minus'] = False
df1 = pd.read_excel('问题1-铅钡高钾组合数据.xlsx', sheet_name='铅钡-风化')
df2 = pd.read_excel('问题1-铅钡高钾组合数据.xlsx', sheet_name='铅钡-未风化')
fig = plt.figure(1)
ax = fig.add_subplot(2, 2, 1)
SiO2 = df1['二氧化硅(SiO2)'].values.flatten()
stats.probplot(SiO2, plot=ax)
obj = ax.findobj(match=plt.Line2D)
obj[0].set(color='black', marker='+', markersize=8, zorder=2)
obj[1].set(color='#D58300', linewidth=1.5, zorder=1)
ax.set_title('SiO2-铅钡-已风化')
ax = fig.add_subplot(2, 2, 2)
SiO2 = df2['二氧化硅(SiO2)'].values.flatten()
stats.probplot(SiO2, plot=ax)
obj = ax.findobj(match=plt.Line2D)
obj[0].set(color='black', marker='+', markersize=8, zorder=2)
obj[1].set(color='#D58300', linewidth=1.5, zorder=1)
ax.set_title('SiO2-铅钡-未风化')
ax = fig.add_subplot(2, 2, 3)
SiO2 = df1['二氧化硅(SiO2)'].values.flatten()
sns.histplot(SiO2, kde=True, color='tab:blue', ax=ax)
ax.set_title('SiO2-铅钡-已风化')
ax = fig.add_subplot(2, 2, 4)
SiO2 = df2['二氧化硅(SiO2)'].values.flatten()
sns.histplot(SiO2, kde=True, color='tab:blue', ax=ax)
ax.set_title('SiO2-铅钡-未风化')
plt.subplots_adjust(hspace=0.5)
plt.show()
