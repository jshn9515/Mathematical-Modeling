import numpy as np
import pandas as pd

alpha = np.deg2rad(1.5)
theta = np.deg2rad(120)
x = np.arange(-800, 1000, 200)
depth = 70 - x * np.tan(alpha)
up = depth * np.sin(theta / 2) * (1 / np.sin(np.pi / 2 - theta / 2 + alpha))
down = depth * np.sin(theta / 2) * (1 / np.sin(np.pi / 2 - theta / 2 - alpha))
width = up + down
overlap = (up[:-1] + down[1:]) * np.cos(alpha) - 200
rate = overlap / width[1:] * 100
rate = np.insert(rate, 0, 0)
index = ['测线距中心点处的距离/m', '海水深度/m', '覆盖宽度/m', '与前一条测线的重叠率/%']
df = pd.DataFrame([x, depth, width, rate], index=index)
df.to_excel('result1.xlsx', header=False, float_format='%.2f')
