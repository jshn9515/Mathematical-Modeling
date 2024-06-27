import numpy as np
import pandas as pd

df1 = pd.read_excel('附件/附件1(Attachment 1)2023-51MCM-Problem B.xlsx', index_col=0)
df_select = df1[['发货城市 (Delivering city)', '收货城市 (Receiving city)']]
count_in, count_out = [], []
receiving_city = df_select['收货城市 (Receiving city)'].unique()
delivering_city = df_select['发货城市 (Delivering city)'].unique()
for city in receiving_city:
    df_temp = df_select[df_select['收货城市 (Receiving city)'] == city]
    count_in.append(df_temp['发货城市 (Delivering city)'].nunique())
for city in delivering_city:
    df_temp = df_select[df_select['发货城市 (Delivering city)'] == city]
    count_out.append(df_temp['收货城市 (Receiving city)'].nunique())
result_in = pd.DataFrame(count_in, index=receiving_city, columns=['上游数'])
result_out = pd.DataFrame(count_out, index=delivering_city, columns=['下游数'])
result = pd.concat([result_in, result_out], axis=1)
result = result.fillna(0).astype(int).sort_index()
result['上下游路径数'] = result['上游数'] + result['下游数']

df2 = pd.read_excel('问题1-城市快递运输量.xlsx', sheet_name='收货量+发货量', index_col=0)
df2_mean = df2.mean()
df2_pct = df2.pct_change()
df2_pct.replace(np.inf, np.nan, inplace=True)
df2_pct_day = df2_pct.mean()
df2_pct.index = df2_pct.index.strftime('%Y-%m')
df2_pct_month = df2_pct.groupby(df2_pct.index).mean()
df2_pct_month.fillna(0, inplace=True)
df2_pct_month = df2_pct_month.mean()
result = pd.concat([result, df2_mean, df2_pct_day, df2_pct_month], axis=1)
result.columns = ['上游数', '下游数', '上下游路径数', '上下游收发量日平均值', '上下游收发量日变化率平均值', '上下游收发量月变化率平均值']
result = result.round(2)
# result.to_excel('城市快递总运输量描述统计.xlsx', index_label='城市')
