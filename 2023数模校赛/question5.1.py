"""
Notes:
    1. In order to increase speed, try to pickle pd.DataFrame first. If you read directly
from .xlsx file, it will be very slow. The following code enable parallel computing, with all
CPU cores used. In this case, 16.
"""

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.multiclass import OutputCodeClassifier
from sklearn.metrics import confusion_matrix

plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['font.size'] = 12

# select dataset
df1 = pd.read_excel('问题5-筛选后训练数据.xlsx', index_col=0)
df2 = pd.read_excel('问题5-筛选后测试数据.xlsx', index_col=0)
train = df1.iloc[:, :-1].values
label = df1.iloc[:, -1].values
Mdl = OutputCodeClassifier(DecisionTreeClassifier(), n_jobs=16)
t1 = time.time()
Mdl.fit(train, label)
t2 = time.time()
print(f'Training time: {t2 - t1:.2f}s')
test = df2.iloc[:, :-1].values
label = df2.iloc[:, -1].values
predict = Mdl.predict(test)
print('R2 score: %.4f' % Mdl.score(test, label))
matrix = confusion_matrix(label, predict)
plt.figure(2)
ticks = np.arange(1, 13)
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
