import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
from sklearn.svm import SVC
from sklearn.multiclass import OutputCodeClassifier
from sklearn.metrics import confusion_matrix
from imblearn.under_sampling import RandomUnderSampler

plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['font.size'] = 12

df1 = pd.read_excel('问题1-筛选后训练数据.xlsx', index_col=0)
df2 = pd.read_excel('问题1-筛选后测试数据.xlsx', index_col=0)

idx = np.array((1 <= df1.y) & (df1.y <= 3))
df1_select: pd.DataFrame = df1.iloc[idx, :]
train = df1_select.iloc[:, :-1].values
label = df1_select.y.values
sample = RandomUnderSampler()
train, label = sample.fit_resample(train, label)
Mdl = OutputCodeClassifier(SVC(C=1, kernel='rbf', verbose=False), n_jobs=16)
Mdl.fit(train, label)
idx = np.array((1 <= df2.y) & (df2.y <= 3))
df2_select: pd.DataFrame = df2.iloc[idx, :]
test = df2_select.iloc[:, :-1].values
label = df2_select.y.values
test, label = sample.fit_resample(test, label)
predict = Mdl.predict(test)
print('Training accuracy: %.4f' % Mdl.score(test, label))
matrix = confusion_matrix(label, predict)
plt.figure(1)
mask = np.bitwise_or(matrix == 0, np.eye(matrix.shape[0], dtype=bool))
cmap = plt.get_cmap('Reds')
cmap = cmap(np.linspace(0.1, 0.8, 256))
cmap = mcolors.LinearSegmentedColormap.from_list('Reds', cmap)
sns.heatmap(matrix, mask=mask, annot=True, fmt='d', cmap=cmap, linewidths=0.5, linecolor='gray',
            cbar=False, xticklabels=['1', '2', '3'], yticklabels=['1', '2', '3'])
mask = np.bitwise_not(np.eye(matrix.shape[0], dtype=bool))
cmap = plt.get_cmap('Blues')
cmap = cmap(np.linspace(0.1, 0.8, 256))
cmap = mcolors.LinearSegmentedColormap.from_list('Blues', cmap)
sns.heatmap(matrix, mask=mask, annot=True, fmt='d', cmap=cmap, linewidths=0.5, linecolor='gray',
            cbar=False, xticklabels=['1', '2', '3'], yticklabels=['1', '2', '3'])
plt.xlabel('Predicted Class')
plt.ylabel('True Class')
plt.show()
