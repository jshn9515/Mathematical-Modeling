import numpy as np
import pandas as pd
from scipy import stats


def calculate(df: pd.DataFrame):
    res_min = df.mean(axis=0) - 3 * df.std(axis=0)
    res_max = df.mean(axis=0) + 3 * df.std(axis=0)
    result = pd.concat([res_min, res_max], axis='columns', keys=['left', 'right'])
    return result


np.set_printoptions(4)
df = pd.read_excel('问题1-铅钡高钾组合数据.xlsx', sheet_name='铅钡-风化', usecols='C:J')
result = calculate(df)
print('The statistic result is: \n', result.round(2))
df = (df - df.mean()) / df.std()
p = np.zeros(df.shape[1])
for i in range(df.shape[1]):
    p[i] = stats.kstest(df.iloc[:, i], stats.norm.cdf)[1]
print('The K-S test result is: ', p)
