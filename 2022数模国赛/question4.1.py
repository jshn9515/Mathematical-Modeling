import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import scipy.stats as stats
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['DengXian']
plt.rcParams['font.size'] = 12
plt.rcParams['axes.unicode_minus'] = False
df1 = pd.read_excel('问题1-铅钡高钾拆分数据.xlsx', sheet_name='铅钡', index_col=0)
df1.drop(columns=['类型', '表面风化'], inplace=True)
df2 = pd.read_excel('问题1-铅钡高钾拆分数据.xlsx', sheet_name='高钾', index_col=0)
df2.drop(columns=['类型', '表面风化'], inplace=True)
label = df1.columns.to_list()
df1.fillna(0, inplace=True)
df2.fillna(0, inplace=True)
rho1, pval1 = stats.spearmanr(df1.values)
rho1 = np.asarray(rho1)
rho2, pval2 = stats.spearmanr(df2.values)
rho2 = np.asarray(rho2)

cmap = plt.get_cmap('RdBu')
cmap = cmap(np.linspace(0.1, 0.9, 256))
cmap = ListedColormap(cmap)
plt.figure(1)
sns.heatmap(rho1, annot=True, fmt='.2f', cmap=cmap, xticklabels=label, yticklabels=label, vmin=-0.6, vmax=0.8)
plt.xticks(rotation=25)
plt.title('铅钡-相关系数', fontsize=15)
plt.figure(2)
sns.heatmap(rho2, annot=True, fmt='.2f', cmap=cmap, xticklabels=label, yticklabels=label, vmin=-0.8, vmax=1)
plt.xticks(rotation=25)
plt.title('高钾-相关系数', fontsize=15)
plt.show()
