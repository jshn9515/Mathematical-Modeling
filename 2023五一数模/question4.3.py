import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DengXian']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12
df = pd.read_excel('问题4-城市快递运输费用.xlsx', sheet_name='敏感性检验', index_col=0)
df.plot()
plt.title('快递运输费用敏感性检验', fontsize=16)
plt.show()
