import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as cluster

np.set_printoptions(4)
title = '未风化'
plt.rcParams['font.sans-serif'] = ['DengXian']
plt.rcParams['font.size'] = 15
df1 = pd.read_excel('问题2-铅钡高钾聚类数据.xlsx', sheet_name=f'铅钡-{title}-聚类')
df2 = pd.read_excel('问题2-铅钡高钾聚类数据.xlsx', sheet_name=f'高钾-{title}-聚类')
df1 = df1.fillna(0)
df2 = df2.fillna(0)
label1 = df1['文物编号'].values
label2 = df2['文物编号'].values
data1 = df1.iloc[:, 3:17]
data2 = df2.iloc[:, 3:17]
Z1: np.ndarray = cluster.linkage(data1, method='average')
Z2: np.ndarray = cluster.linkage(data2, method='average')
T1 = cluster.fcluster(Z1, 3, criterion='maxclust')
T2 = cluster.fcluster(Z2, 3, criterion='maxclust')
print('The cluster result for the first one is: ', T1)
print('The cluster result for the second one is: ', T2)
noise1 = np.random.randn(df1.shape[0], 2)
noise2 = np.random.randn(df2.shape[0], 3)
plt.figure(1)
cluster.dendrogram(Z1, labels=label1, color_threshold='default')
plt.xticks(rotation=30, horizontalalignment='right', fontsize=15)
plt.title(f'铅钡-{title}-聚类图')
plt.figure(2)
cluster.dendrogram(Z2, labels=label2)
plt.xticks(rotation=30, horizontalalignment='right', fontsize=15)
plt.title(f'高钾-{title}-聚类图')
x1 = np.arange(0, Z1.shape[0])
x2 = np.arange(0, Z2.shape[0])
y1 = sorted(Z1[:, 2], reverse=True)
y2 = sorted(Z2[:, 2], reverse=True)
plt.figure(3)
plt.plot(x1, y1, linewidth=2)
plt.title(f'铅钡-{title}-样本距离图')
plt.figure(4)
plt.plot(x2, y2, linewidth=2)
plt.title(f'高钾-{title}-样本距离图')
plt.show()
