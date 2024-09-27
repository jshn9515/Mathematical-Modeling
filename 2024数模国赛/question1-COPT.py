import numpy as np
import pandas as pd
import coptpy as cp

df1 = pd.read_excel('附件1.xlsx', sheet_name='乡村的现有耕地', index_col=0, usecols='A:C')
df1 = pd.concat([df1, df1.loc['D1':'F4']], axis=0)

df2 = pd.read_excel('问题1-农作物汇总表.xlsx', sheet_name='销售单价', index_col=[0, 1])
df2.fillna(0, inplace=True)
df3 = pd.read_excel('问题1-农作物汇总表.xlsx', sheet_name='种植成本', index_col=[0, 1])
df3.fillna(0, inplace=True)
df4 = pd.read_excel('问题1-农作物汇总表.xlsx', sheet_name='亩产量', index_col=[0, 1])
df4.fillna(0, inplace=True)
df5 = pd.read_excel('问题1-农作物汇总表.xlsx', sheet_name='种植面积', index_col=[0, 1])
df5.fillna(0, inplace=True)
year = 7
env = cp.Envr()
model = env.createModel('crop')
x = model.addMVar((82, 41, year), nameprefix='农作物种植面积')
b = model.addVars(8, vtype=cp.COPT.BINARY, nameprefix='水浇地是否为单季种植')

max_crop = np.sum(df4.values * df5.values, axis=0)
model.addConstrs(x[:26, 15:, :] == 0, nameprefix='平旱地_梯田_山坡地')

for k in range(year):
    for i in range(8):
        for j in x[26 + i, :15, k].tolist():
            model.addGenConstrIndicator(b[i], True, j == 0, name='水浇地_单季')
        for j in x[26 + i, 16:, k].tolist():
            model.addGenConstrIndicator(b[i], True, j == 0, name='水浇地_单季')
        for j in x[26 + i, :15, k].tolist():
            model.addGenConstrIndicator(b[i], False, j == 0, name='水浇地_第一季')
        for j in x[26 + i, 34:, k].tolist():
            model.addGenConstrIndicator(b[i], False, j == 0, name='水浇地_第一季')
        for j in x[54 + i, :33, k].tolist():
            model.addGenConstrIndicator(b[i], False, j == 0, name='水浇地_第二季')
        for j in x[54 + i, 37:, k].tolist():
            model.addGenConstrIndicator(b[i], False, j == 0, name='水浇地_第二季')
    model.addConstrs(x[34 : 54, :15, k] == 0, nameprefix='普通大棚_智慧大棚_第一季')
    model.addConstrs(x[34 : 54, 34:, k] == 0, nameprefix='普通大棚_智慧大棚_第一季')
    model.addConstrs(x[62 : 78, :37, k] == 0, nameprefix='普通大棚_第二季')
    model.addConstrs(x[78:, :15, k] == 0, nameprefix='智慧大棚_第二季')
    model.addConstrs(x[78:, 34:, k] == 0, nameprefix='智慧大棚_第二季')
    model.addConstrs(x[:, :, k].sum(axis=1) <= df1['地块面积/亩'].to_numpy(), nameprefix='种植面积')
    model.addConstrs((x[:, :, k] * df4.values).sum(axis=0) <= max_crop, nameprefix='最大产量限制')

bean = np.array([1, 2, 3, 4, 5, 17, 18, 19]) - 1
for k in range(year - 1):
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            model.addSOS(cp.COPT.SOS_TYPE1, x[i, j, k : k + 2].tolist())
for k in range(year - 3):
    for i in range(x.shape[0]):
        for j in bean:
            model.addSOS(cp.COPT.SOS_TYPE1, x[i, j, k : k + 3].tolist())

profit = np.zeros((82, 41), dtype=object)
profit = cp.MLinExpr(profit)
for k in range(year):
    profit += df4.values * x[:, :, k] * df2.values
    profit -= x[:, :, k] * df3.values
model.setObjective(profit.sum(), sense=cp.COPT.MAXIMIZE)
model.setParam('RelGap', 0.0001)
model.solve()

with pd.ExcelWriter('问题1-结果.xlsx', mode='w') as fp:
    for k in range(year):
        file = pd.DataFrame(np.round(x[:, :, k].x, 2), index=df5.index, columns=df5.columns)
        file.to_excel(fp, sheet_name=f'{2024 + k}')
