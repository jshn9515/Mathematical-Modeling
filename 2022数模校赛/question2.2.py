import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.size'] = 12
df = pd.read_excel('问题1-毒蘑菇和无毒蘑菇各指标总数.xlsx', index_col=0)
data = df['毒蘑菇占比']
plt.figure(1)
h = plt.bar(data.index, data.values, width=0.5, edgecolor='black', linewidth=0.8, alpha=0.8)
plt.bar_label(h, fmt='%.2f', fontsize=10)
plt.xticks(rotation=25)
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)
plt.title('The proportion of poisonous mushrooms')
plt.show()
