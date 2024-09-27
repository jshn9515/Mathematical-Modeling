import pandas as pd

df = pd.read_excel('表2 2000-2023年山东省各气象站点日观测.xlsx', index_col=0,
                   na_values=['99.99', '999.9', '9999.9'])
df.to_pickle('表2 2000-2023年山东省各气象站点日观测.pkl')
