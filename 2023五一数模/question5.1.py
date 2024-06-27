import pandas as pd

df = pd.read_excel('附件/附件2(Attachment 2)2023-51MCM-Problem B.xlsx', index_col=0)
df.rename(columns={'快递运输数量(件) (Express delivery quantity (PCS))': '快递运输数量(件)'}, inplace=True)
time = df.index.unique()
result = pd.DataFrame()
receiving_city = df['收货城市 (Receiving city)'].unique()
for city1 in receiving_city:
    df_temp1 = df[df['收货城市 (Receiving city)'] == city1]
    delivering_city = df_temp1['发货城市 (Delivering city)'].unique()
    for city2 in delivering_city:
        df_result = pd.DataFrame(index=time)
        df_temp2 = df_temp1[df_temp1['发货城市 (Delivering city)'] == city2]
        df_result = df_result.join(df_temp2, how='left')
        df_result['收货城市 (Receiving city)'] = city1
        df_result['发货城市 (Delivering city)'] = city2
        df_result.fillna(0, inplace=True)
        result = pd.concat((result, df_result), axis=0)
result.columns = df.columns
result.sort_index(inplace=True)
result['快递运输数量(件)'] = result['快递运输数量(件)'].astype(int)
result['快递运输路线'] = result['发货城市 (Delivering city)'] + result['收货城市 (Receiving city)']
result.drop(columns=['发货城市 (Delivering city)', '收货城市 (Receiving city)'], inplace=True)
result = result.reindex(columns=['快递运输路线', '快递运输数量(件)'])
# result.to_excel('发货数量统计表.xlsx', index_label='日期(年/月/日) (Date Y/M/D)')
