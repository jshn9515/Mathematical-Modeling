import numpy as np
import pandas as pd

df1 = pd.read_excel('问题5-发货数量统计.xlsx', index_col=0)
df2 = pd.read_excel('问题5-固定需求常数.xlsx', index_col=0)
df1['年份'] = df1.index.year
df1['季度'] = np.ceil(df1.index.month / 3).astype(int)
df1 = df1.reindex(columns=['年份', '季度', '快递运输路线', '快递运输数量(件)'])
df3 = df1.merge(df2, how='left', on=['年份', '季度', '快递运输路线'])
df3.index = df1.index
df3.to_excel('发货数量与固定需求常数统计表.xlsx', float_format='%.0f')
