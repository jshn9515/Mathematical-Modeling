import pandas as pd

df: pd.DataFrame = pd.read_pickle('表2 2000-2023年山东省各气象站点日观测.pkl')
df1 = pd.read_excel('表1 2000-2022年山东省主要农作物年产量.xlsx', index_col=0)
df1['总产量(万吨)'] = df1.sum(axis=1)
df2 = pd.read_excel('表3 2000-2022年山东省年均日照时数.xlsx', index_col=0)
df3 = pd.read_excel('表4 2000-2023年逐日太阳黑子数.xlsx', index_col=0)
var = ['TEMP', 'DEWP', 'SLP', 'STP', 'VISIB', 'WDSP', 'MXSPD', 'MAX', 'MIN', 'PRCP', 'SNDP']
df = df[var]
resample = df.resample('YS')
df = resample.mean()
df['PRCP'] = resample['PRCP'].sum()
df.index = df.index.year
df.rename_axis('YEAR', inplace=True)
df3 = df3.resample('YS').mean()
df3.index = df3.index.year
df = pd.concat([df, df2, df3, df1], axis=1)
df.drop(index=2023, inplace=True)
df.fillna(0, inplace=True)
# df.to_excel('问题2-山东省农业气象数据汇总表.xlsx', index_label='YEAR', float_format='%.2f')
