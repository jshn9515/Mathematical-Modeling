import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['DengXian']
plt.rcParams['font.size'] = 12
plt.rcParams['axes.unicode_minus'] = False
df: pd.DataFrame = pd.read_pickle('附件1-原始训练数据.pkl')
var = np.loadtxt('问题1-筛选变量名称.txt', dtype=str)
fig, ax = plt.subplots(4, 3)
ax = ax.flatten()
plt.delaxes(ax[-2])
plt.delaxes(ax[-1])
for i in range(len(var)):
    idx = np.empty((df.shape[0], 3), dtype=bool)
    idx[:, 0] = (1 <= df.y) & (df.y <= 3)
    idx[:, 1] = (4 <= df.y) & (df.y <= 6)
    idx[:, 2] = (7 <= df.y) & (df.y <= 12)
    assert np.all(np.sum(idx, axis=1) == 1)
    for j in range(3):
        data = df.loc[idx[:, j], var[i]]
        x = np.linspace(data.min(), data.max(), 1000)
        sns.kdeplot(data, ax=ax[i], fill=True)
fig.legend(['动态活动', '静态姿势', '静态姿势转换'], bbox_to_anchor=(0.52, 0.25), fontsize=14)
plt.subplots_adjust(hspace=0.5)
plt.show()
