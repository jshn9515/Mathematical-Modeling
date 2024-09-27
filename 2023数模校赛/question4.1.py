import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import RocCurveDisplay, confusion_matrix

plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['font.size'] = 12

df1: pd.DataFrame = pd.read_pickle('附件1-原始训练数据.pkl')
df2: pd.DataFrame = pd.read_pickle('附件2-原始测试数据.pkl')
ticks = ['8', '9']

idx = np.array((df1.y == ticks[0]) | (df1.y == ticks[1]))
df1_select: pd.DataFrame = df1.iloc[idx, :]
train = df1_select.iloc[:, :-1].values
label = df1_select.y.values
Mdl = RandomForestClassifier(n_estimators=50, n_jobs=16, oob_score=True, max_features=None, verbose=False)
Mdl.fit(train, label)
idx = np.array((df2.y == ticks[0]) | (df2.y == ticks[1]))
df2_select: pd.DataFrame = df2.iloc[idx, :]
test = df2_select.iloc[:, :-1].values
label = df2_select.y.values
predict = Mdl.predict(test)
print('Training accuracy: %.4f' % Mdl.score(test, label))
matrix = confusion_matrix(label, predict)
plt.figure(1)
mask = np.bitwise_or(matrix == 0, np.eye(matrix.shape[0], dtype=bool))
cmap = plt.get_cmap('Reds')
cmap = cmap(np.linspace(0.1, 0.8, 256))
cmap = mcolors.LinearSegmentedColormap.from_list('Reds', cmap)
sns.heatmap(matrix, mask=mask, annot=True, fmt='d', cmap=cmap, linewidths=0.5, linecolor='gray',
            cbar=False, xticklabels=ticks, yticklabels=ticks)
mask = np.bitwise_not(np.eye(matrix.shape[0], dtype=bool))
cmap = plt.get_cmap('Blues')
cmap = cmap(np.linspace(0.1, 0.8, 256))
cmap = mcolors.LinearSegmentedColormap.from_list('Blues', cmap)
sns.heatmap(matrix, mask=mask, annot=True, fmt='d', cmap=cmap, linewidths=0.5, linecolor='gray',
            cbar=False, xticklabels=ticks, yticklabels=ticks)
plt.xlabel('Predicted Class')
plt.ylabel('True Class')
fig = plt.figure(2)
ax = fig.add_subplot(1, 1, 1)
RocCurveDisplay.from_estimator(Mdl, test, label, plot_chance_level=True, color='darkorange',  # noqa
                               name='RandomForestClassifier', ax=ax)
plt.show()
