import pandas as pd
import scipy.stats as stats

df3 = pd.read_excel('问题1-卡方检验.xlsx', index_col=0, usecols='A:C')  # noqa
data1 = df3.iloc[0:2, :].to_numpy(float)
data2 = df3.iloc[4:7, :].to_numpy(float)
data3 = df3.iloc[9:17, :].to_numpy(float)
p1 = stats.chi2_contingency(data1)[1]
p2 = stats.chi2_contingency(data2)[1]
p3 = stats.chi2_contingency(data3)[1]
print(f'The chi2test result is: {p1:.4f}, {p2:.4f}, {p3:.4f}')
