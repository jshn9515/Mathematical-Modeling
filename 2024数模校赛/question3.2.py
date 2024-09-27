import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DengXian']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12
df = pd.read_excel('问题2-山东省农业气象数据汇总表.xlsx', index_col=0)
X = df.iloc[:, :13]
X = sm.add_constant(X)
noise = np.arange(-2.0, 3.0, 1.0)
result = []
for i in range(13, 17):
    y = df.iloc[:, i]
    Mdl = sm.GLM(y, X)
    Mdl = Mdl.fit()
    for inc in noise:
        reduce = df.iloc[-1, :13].to_numpy()
        reduce = np.insert(reduce, 0, 1.0)
        reduce[-1] += inc
        predict = Mdl.predict(reduce)
        result.append(predict)
result = np.array(result)
result = np.reshape(result, (4, len(noise)))
fig, ax = plt.subplots(2, 2)
var = [['稻谷'], ['小麦'], ['玉米'], ['大豆']]
ax = ax.flatten()
for i in range(len(ax)):
    ax[i].plot(noise, result[i])
    ax[i].set_xlabel('极端高温变化天数')
    ax[i].set_ylabel('产量')
    ax[i].legend(var[i])
plt.show()
