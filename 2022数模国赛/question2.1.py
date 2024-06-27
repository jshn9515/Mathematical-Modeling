import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DengXian']
plt.rcParams['font.size'] = 15
label = ['二氧化硅(SiO2)', '氧化钙(CaO)', '氧化铝(Al2O3)', '氧化铜(CuO)', '五氧化二磷(P2O5)']
x = np.arange(len(label))
K_wind = pd.read_excel('问题1-铅钡高钾组合数据.xlsx', sheet_name='高钾-风化', usecols='C:I', nrows=6)  # noqa
K_wind = K_wind.iloc[:, [0, 2, 3, 5, 6]].values
K_wind = np.mean(K_wind, axis=0)
K = pd.read_excel('问题1-铅钡高钾组合数据.xlsx', sheet_name='高钾-未风化', usecols='C:I', nrows=12)  # noqa
K = K.iloc[:, [0, 2, 3, 5, 6]].values
K = np.mean(K, axis=0)
PbBa_wind = pd.read_excel('问题1-铅钡高钾组合数据.xlsx', sheet_name='铅钡-风化', usecols='C:J', nrows=27)  # noqa
PbBa_wind = PbBa_wind.iloc[:, [0, 1, 2, 3, 7]].values
PbBa_wind = np.mean(PbBa_wind, axis=0)
PbBa = pd.read_excel('问题1-铅钡高钾组合数据.xlsx', sheet_name='铅钡-未风化', usecols='C:J', nrows=22)  # noqa;
PbBa = PbBa.iloc[:, [0, 1, 2, 3, 7]].values
PbBa = np.mean(PbBa, axis=0)
fig = plt.figure(1)
ax1 = fig.add_subplot(1, 1, 1)
ax2 = ax1.twinx()
width = 0.2
rects = ax1.bar(x[:1], K[:1], width=width, label='高钾玻璃', color='#338ECA', edgecolor='black', linewidth=0.9)
ax1.bar_label(rects, padding=3, fmt='%.2f')
rects = ax2.bar(x[1:], K[1:], width=width, label='高钾玻璃', color='#FFCD33', edgecolor='black', linewidth=0.9)
ax2.bar_label(rects, padding=3, fmt='%.2f')
rects = ax1.bar(x[:1] + width + 0.05, PbBa[:1], width=width, label='铅钡玻璃', color='#E17547', edgecolor='black', linewidth=0.9)
ax1.bar_label(rects, padding=3, fmt='%.2f')
rects = ax2.bar(x[1:] + width + 0.05, PbBa[1:], width=width, label='铅钡玻璃', color='#B7B7B7', edgecolor='black', linewidth=0.9)
ax2.bar_label(rects, padding=3, fmt='%.2f')
ax1.set_ylabel('含量(单位: %)')
ax2.set_ylabel('含量(单位: %)', rotation=-90, labelpad=15)
ax1.set_yticks(np.arange(0, 80, 10))
ax1.set_ylim(0, 70)
ax2.set_yticks(np.arange(0, 8, 1))
ax2.set_ylim(0, 7)
plt.title('未风化高钾玻璃铅钡玻璃元素对比')
plt.xticks(x + width / 2 + 0.025, label)
plt.grid(axis='y', linewidth=0.6, linestyle='-', alpha=0.5)
plt.legend(loc='upper right')
fig = plt.figure(2)
ax1 = fig.add_subplot(1, 1, 1)
ax2 = ax1.twinx()
width = 0.2
rects = ax1.bar(x[:1], K_wind[:1], width=width, label='高钾玻璃', color='#338ECA', edgecolor='black', linewidth=0.9)
ax1.bar_label(rects, padding=3, fmt='%.2f')
rects = ax2.bar(x[1:], K_wind[1:], width=width, label='高钾玻璃', color='#FFCD33', edgecolor='black', linewidth=0.9)
ax2.bar_label(rects, padding=3, fmt='%.2f')
rects = ax1.bar(x[:1] + width + 0.05, PbBa_wind[:1], width=width, label='铅钡玻璃', color='#E17547', edgecolor='black', linewidth=0.9)
ax1.bar_label(rects, padding=3, fmt='%.2f')
rects = ax2.bar(x[1:] + width + 0.05, PbBa_wind[1:], width=width, label='铅钡玻璃', color='#B7B7B7', edgecolor='black', linewidth=0.9)
ax2.bar_label(rects, padding=3, fmt='%.2f')
ax1.set_ylabel('含量(单位: %)')
ax2.set_ylabel('含量(单位: %)', rotation=-90, labelpad=15)
ax1.set_yticks(np.arange(0, 110, 10))
ax1.set_ylim(0, 100)
ax2.set_yticks(np.arange(0, 8, 1))
ax2.set_ylim(0, 7)
plt.title('已风化高钾玻璃铅钡玻璃元素对比')
plt.xticks(x + width / 2 + 0.025, label)
plt.grid(axis='y', linewidth=0.6, linestyle='-', alpha=0.5)
plt.legend(loc='upper right')
plt.show()
