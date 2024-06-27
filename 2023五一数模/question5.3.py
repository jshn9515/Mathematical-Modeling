import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity

plt.rcParams['font.sans-serif'] = ['DengXian']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12
df = pd.read_excel('问题5-发货数量与固定需求常数统计表.xlsx', sheet_name='筛选后', index_col=0)
Mdl = KernelDensity(kernel='gaussian', bandwidth=0.5)
fig, ax = plt.subplots(2, 2)
ax = ax.flatten()
route = ['VN', 'VQ', 'JI', 'OG']
for i in range(len(route)):
    data = df.loc[df['快递运输路线'] == route[i], '非固定需求常数'].values.reshape(-1, 1)
    data_plot = np.linspace(np.min(data), np.max(data), 1000).reshape(-1, 1)
    Mdl.fit(data)
    log_density = Mdl.score_samples(data_plot)
    ax[i].hist(data, bins=30, density=True, color='#b7b7b7')
    ax[i].plot(data_plot, np.exp(log_density), linewidth=1.2)
    ax[i].set_xlabel('非固定需求常数')
    ax[i].set_ylabel('概率密度')
    ax[i].legend(['核密度估计', '频率直方图'], loc='upper right')
    ax[i].set_title(f'快递运输路线：{repr(route[i])}')
plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.4, hspace=0.4)
plt.suptitle('非固定需求常数的核密度估计图', fontsize=16)
plt.show()
