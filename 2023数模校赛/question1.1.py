"""
Notes:
    1. In order to increase speed, try to pickle pd.DataFrame first. If you read directly
from .xlsx file, it will be very slow. The following code enable parallel computing, with all
CPU cores used. In this case, 16.
    2. There exist certain discrepancies between the Python and MATLAB implementations of
RandomForest, leading to variations in the results. The MATLAB version exhibits superior
numerical stability and delivers more precise outcomes.
"""

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['font.size'] = 12
# entire dataset
df1: pd.DataFrame = pd.read_pickle('附件1-原始训练数据.pkl')
df2: pd.DataFrame = pd.read_pickle('附件2-原始测试数据.pkl')
train = df1.iloc[:, :-1].to_numpy()
label = df1.iloc[:, -1].to_numpy()
name = df1.columns.values
Mdl = RandomForestClassifier(n_estimators=50, n_jobs=16, oob_score=True, max_features=None, verbose=True)
t1 = time.time()
Mdl.fit(train, label)
t2 = time.time()
print(f'Training time: {t2 - t1:.2f}s')
importance = Mdl.feature_importances_
idx = np.argsort(-importance)
name = name[idx[:10]]
# print('Top 10 important variables:\n', name)
np.savetxt('问题1-筛选变量名称.txt', name, fmt='%s')
test = df2.iloc[:, :-1].to_numpy()
label = df2.iloc[:, -1].to_numpy()
predict = Mdl.predict(test)
print('R2 score: %.4f' % Mdl.score(test, label))
matrix = confusion_matrix(label, predict)
plt.figure(1)
ticks = list(map(str, range(1, 13)))
mask = np.bitwise_or(matrix == 0, np.eye(matrix.shape[0], dtype=bool))
cmap = plt.get_cmap('Reds')
cmap = cmap(np.linspace(0.1, 0.8, 256))
cmap = mcolors.LinearSegmentedColormap.from_list('Reds', cmap)
sns.heatmap(matrix, mask=mask, annot=True, fmt='d', cmap=cmap, linewidths=0.5, linecolor='gray',
            xticklabels=ticks, yticklabels=ticks, cbar=False)
mask = np.bitwise_not(np.eye(matrix.shape[0], dtype=bool))
cmap = plt.get_cmap('Blues')
cmap = cmap(np.linspace(0.1, 0.8, 256))
cmap = mcolors.LinearSegmentedColormap.from_list('Blues', cmap)
sns.heatmap(matrix, mask=mask, annot=True, fmt='d', cmap=cmap, linewidths=0.5, linecolor='gray',
            xticklabels=ticks, yticklabels=ticks, cbar=False)
plt.xlabel('Predicted Class')
plt.ylabel('True Class')

# select dataset
name = np.hstack((name, 'y'))
df1: pd.DataFrame = df1[name]
df2: pd.DataFrame = df2[name]
train = df1.iloc[:, :-1].to_numpy()
label = df1.iloc[:, -1].to_numpy()
Mdl = RandomForestClassifier(n_estimators=50, n_jobs=16, oob_score=True, max_features=None, verbose=False)
t1 = time.time()
Mdl.fit(train, label)
t2 = time.time()
print(f'Training time: {t2 - t1:.2f}s')
test = df2.iloc[:, :-1].to_numpy()
label = df2.iloc[:, -1].to_numpy()
predict = Mdl.predict(test)
print('R2 score: %.4f' % Mdl.score(test, label))
matrix = confusion_matrix(label, predict)
plt.figure(2)
ticks = list(map(str, range(1, 13)))
mask = np.bitwise_or(matrix == 0, np.eye(matrix.shape[0], dtype=bool))
cmap = plt.get_cmap('Reds')
cmap = cmap(np.linspace(0.1, 0.8, 256))
cmap = mcolors.LinearSegmentedColormap.from_list('Reds', cmap)
sns.heatmap(matrix, mask=mask, annot=True, fmt='d', cmap=cmap, linewidths=0.5, linecolor='gray',
            xticklabels=ticks, yticklabels=ticks, cbar=False)
mask = np.bitwise_not(np.eye(matrix.shape[0], dtype=bool))
cmap = plt.get_cmap('Blues')
cmap = cmap(np.linspace(0.1, 0.8, 256))
cmap = mcolors.LinearSegmentedColormap.from_list('Blues', cmap)
sns.heatmap(matrix, mask=mask, annot=True, fmt='d', cmap=cmap, linewidths=0.5, linecolor='gray',
            xticklabels=ticks, yticklabels=ticks, cbar=False)
plt.xlabel('Predicted Class')
plt.ylabel('True Class')
plt.show()
