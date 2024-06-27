import pandas as pd

df = pd.read_excel('secondary_data.xlsx')
pivot = df.pivot_table(index='class', aggfunc='count').T
print(pivot)
# pivot.to_excel('毒蘑菇和无毒蘑菇各指标总数.xlsx')
