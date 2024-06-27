import pandas as pd

df = pd.read_excel('附件/附件1(Attachment 1)2023-51MCM-Problem B.xlsx', index_col=0)
time_range = df.index
df_in = df.drop(columns='发货城市 (Delivering city)')
df_out = df.drop(columns='收货城市 (Receiving city)')
tab_in = pd.pivot_table(df_in, index=['日期(年/月/日) (Date Y/M/D)', '收货城市 (Receiving city)'], aggfunc='sum')
tab_out = pd.pivot_table(df_out, index=['日期(年/月/日) (Date Y/M/D)', '发货城市 (Delivering city)'], aggfunc='sum')
result_in = pd.DataFrame(index=time_range.unique())
result_out = pd.DataFrame(index=time_range.unique())
for city_in in df_in['收货城市 (Receiving city)'].unique():
    tab_city_in = tab_in[tab_in.index.get_level_values(1) == city_in]
    tab_city_in_drop = tab_city_in.reset_index(1, drop=True)
    tab_city_in_drop.rename(columns={'快递运输数量(件) (Express delivery quantity (PCS))': city_in}, inplace=True)
    result_in = result_in.join(tab_city_in_drop, how='left')
for city_out in df_out['发货城市 (Delivering city)'].unique():
    tab_city_out = tab_out[tab_out.index.get_level_values(1) == city_out]
    tab_city_out_drop = tab_city_out.reset_index(1, drop=True)
    tab_city_out_drop.rename(columns={'快递运输数量(件) (Express delivery quantity (PCS))': city_out}, inplace=True)
    result_out = result_out.join(tab_city_out_drop, how='left')
result_in.fillna(0, inplace=True)
result_in.sort_index(axis=1, inplace=True)
result_out.fillna(0, inplace=True)
result_out.sort_index(axis=1, inplace=True)
result = result_in + result_out
# result_in.to_excel('收货城市快递运输量.xlsx')
# result_out.to_excel('发货城市快递运输量.xlsx')
# result.to_excel('城市快递总运输量.xlsx')
result_in_stat = result_in.describe().T.round(2)
result_out_stat = result_out.describe().T.round(2)
# result_in_solve.to_excel('收货城市快递运输量描述统计.xlsx', index_label='城市')
# result_out_solve.to_excel('发货城市快递运输量描述统计.xlsx', index_label='城市')
