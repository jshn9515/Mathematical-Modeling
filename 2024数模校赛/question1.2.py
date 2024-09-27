import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DengXian']
plt.rcParams['font.size'] = 15
plt.rcParams['axes.unicode_minus'] = False
df = pd.read_excel('表1 2000-2022年山东省主要农作物年产量.xlsx', index_col=0)
index = df.columns.str.slice(0, -4).to_list()
corr = df.corr(method='spearman')
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=1, linecolor='white',
            xticklabels=index, yticklabels=index)
plt.show()
