"""
This file demonstrate how to pickle pd.DataFrame to speed up the reading process.
"""

import pandas as pd

df1 = pd.read_excel('附件2-原始测试数据.xlsx', index_col=0)
df2 = pd.read_excel('附件2-测试数据标签.xlsx', index_col=0)
df = pd.concat([df1, df2], axis=1)
df.to_pickle('附件2-原始测试数据.pkl')
