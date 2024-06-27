import numpy as np
import pandas as pd


def entropy(Z: np.ndarray) -> np.ndarray:
    Z = np.array(Z)
    Z = Z / np.sum(Z, axis=0)
    Z = np.where(Z == 0, 1, Z)
    weight = 1 + np.sum(Z * np.log(Z), axis=0) / np.log(Z.shape[0])
    weight = weight / np.sum(weight)
    return weight


df1 = pd.read_excel('问题1-城市快递运输量.xlsx', sheet_name='收货统计', index_col=0)
df2 = pd.read_excel('问题1-城市快递运输量.xlsx', sheet_name='发货统计', index_col=0)
df3 = pd.read_excel('问题1-城市快递运输量.xlsx', sheet_name='收货量+发货量统计', index_col=0)
df3.drop(columns=['上游数', '下游数'], inplace=True)
df = pd.concat([df1, df2, df3], axis=1)
data = df.values
Z = data / np.sqrt(np.sum(data ** 2, axis=0))
if np.any(Z < 0):
    Z = (Z - np.min(Z, axis=0)) / (np.max(Z, axis=0) - np.min(Z, axis=0))
weight = entropy(Z)
df_weight = pd.DataFrame(weight, index=df.columns, columns=['权重'])
df_weight.sort_values(by='权重', ascending=False, inplace=True)
# df_weight.to_excel('城市快递运输量权重.xlsx', index_label='指标')
Dp = np.sqrt(np.sum(((Z - np.max(Z, axis=0)) ** 2) * weight, axis=1))
Dn = np.sqrt(np.sum(((Z - np.min(Z, axis=0)) ** 2) * weight, axis=1))
score = Dn / (Dp + Dn)
score = score / np.sum(score)
df_score = pd.DataFrame(score, index=df.index, columns=['得分'])
df_score.sort_values(by='得分', ascending=False, inplace=True)
# df_score.to_excel('城市快递运输量得分.xlsx', index_label='城市')
