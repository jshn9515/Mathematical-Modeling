import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
from sklearn.svm import SVC
from sklearn.multiclass import OutputCodeClassifier
from imblearn.under_sampling import RandomUnderSampler
from sklearn.metrics import confusion_matrix

plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['font.size'] = 12

df1 = pd.read_excel('问题1-筛选后训练数据.xlsx', index_col=0)
df2 = pd.read_excel('问题1-筛选后测试数据.xlsx', index_col=0)

idx = np.array((1 <= df1.y) & (df1.y <= 6))
df1_select = df1.iloc[idx, :]
train = df1_select.iloc[:, :-1].values
label = np.array((1 <= df1_select.y) & (df1_select.y <= 3))
sample = RandomUnderSampler()
train, label = sample.fit_resample(train, label)
Mdl = OutputCodeClassifier(SVC(C=1, kernel='linear', verbose=False), n_jobs=16)
Mdl.fit(train, label)
idx = np.array((1 <= df2.y) & (df2.y <= 6))
df2_select = df2.iloc[idx, :]
test = df2_select.iloc[:, :-1].values
label = np.array((1 <= df2_select.y) & (df2_select.y <= 3))
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
            xticklabels=(0, 1), yticklabels=(0, 1), cbar=False)
mask = np.bitwise_not(np.eye(matrix.shape[0], dtype=bool))
cmap = plt.get_cmap('Blues')
cmap = cmap(np.linspace(0.1, 0.8, 256))
cmap = mcolors.LinearSegmentedColormap.from_list('Blues', cmap)
sns.heatmap(matrix, mask=mask, annot=True, fmt='d', cmap=cmap, linewidths=0.5, linecolor='gray',
            xticklabels=(0, 1), yticklabels=(0, 1), cbar=False)
plt.xlabel('Predicted Class')
plt.ylabel('True Class')
plt.show()
