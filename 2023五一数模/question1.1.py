import pandas as pd
pd.options.mode.copy_on_write = True

df = pd.read_excel('附件/附件1(Attachment 1)2023-51MCM-Problem B.xlsx', index_col=0)
time_range = df.index.unique()
df_in = df.drop(columns='发货城市 (Delivering city)')
df_out = df.drop(columns='收货城市 (Receiving city)')
tab_in = pd.pivot_table(df_in, index=['日期(年/月/日) (Date Y/M/D)', '收货城市 (Receiving city)'], aggfunc='sum')
tab_out = pd.pivot_table(df_out, index=['日期(年/月/日) (Date Y/M/D)', '发货城市 (Delivering city)'], aggfunc='sum')
result_in = pd.DataFrame(index=time_range)
result_out = pd.DataFrame(index=time_range)
for city_in in df_in['收货城市 (Receiving city)'].unique():
    idx = tab_in.index.get_level_values(1) == city_in
    tab_city_in: pd.DataFrame = tab_in[idx]
    tab_city_in.reset_index(1, drop=True, inplace=True)
    mapper = {'快递运输数量(件) (Express delivery quantity (PCS))': city_in}
    tab_city_in.rename(columns=mapper, inplace=True)
    result_in = result_in.join(tab_city_in, how='left')
for city_out in df_out['发货城市 (Delivering city)'].unique():
    idx = tab_out.index.get_level_values(1) == city_out
    tab_city_out: pd.DataFrame = tab_out[idx]
    tab_city_out.reset_index(1, drop=True, inplace=True)
    mapper = {'快递运输数量(件) (Express delivery quantity (PCS))': city_out}
    tab_city_out.rename(columns=mapper, inplace=True)
    result_out = result_out.join(tab_city_out, how='left')
result_in.fillna(0, inplace=True)
result_in.sort_index(axis=1, inplace=True)
result_out.fillna(0, inplace=True)
result_out.sort_index(axis=1, inplace=True)
result = result_in.add(result_out, fill_value=0)
result_in_stat = result_in.describe().T
result_out_stat = result_out.describe().T
save = False
if save:
    with pd.ExcelWriter('问题1-城市快递运输量.xlsx', mode='w') as fp:
        result_in.to_excel(fp, sheet_name='收货')
        result_in_stat.to_excel(fp, sheet_name='收货统计', float_format='%.2f')
        result_out.to_excel(fp, sheet_name='发货')
        result_out_stat.to_excel(fp, sheet_name='发货统计', float_format='%.2f')
        result.to_excel(fp, sheet_name='收货量+发货量')
        