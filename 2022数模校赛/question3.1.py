import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

np.set_printoptions(4)
plt.rcParams['font.size'] = 14
df = pd.read_excel('secondary_data_no_miss.xlsx')
label = df.columns[1:]
target = df['class'].unique().tolist()
encoder = LabelEncoder()
decoder = LabelEncoder()
decoder.fit(df['class'])
data = df.values
for col in range(data.shape[1]):
    data[:, col] = encoder.fit_transform(data[:, col])
data = data.astype(int)
train_data, test_data = train_test_split(data, test_size=0.2)
Mdl = MLPClassifier(batch_size=256, activation='logistic', learning_rate_init=0.01, verbose=True)
Mdl.fit(train_data[:, 1:], train_data[:, 0])
score = Mdl.score(test_data[:, 1:], test_data[:, 0])
curve = Mdl.loss_curve_
print(f'R2 score: {score:.4f}')
predict = Mdl.predict(test_data[:, 1:])
matrix = confusion_matrix(test_data[:, 0], predict)
cmap = plt.get_cmap('Blues')
cmap = cmap(np.arange(0.1, 0.9, 0.1))
cmap = mcolors.LinearSegmentedColormap.from_list('Blues', cmap)
plt.figure(1)
sns.heatmap(matrix, annot=True, fmt='d', cmap=cmap, xticklabels=target, yticklabels=target)
plt.figure(2)
plt.plot(range(len(curve)), curve)
plt.title('The loss curve for iteration')
plt.xlabel('Iteration (times)')
plt.ylabel('Loss value')
plt.show()
