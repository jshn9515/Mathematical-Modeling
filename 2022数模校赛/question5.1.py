import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans

df = pd.read_excel('问题1-蘑菇原始数据.xlsx')
df = df[df['class'] == 'p']
data = df.iloc[:, 1:].values
encoder = LabelEncoder()
for col in range(data.shape[1]):
    data[:, col] = encoder.fit_transform(data[:, col])
data = data.astype(int)
Mdl = KMeans(n_clusters=4)
result = Mdl.fit_predict(data)
result = pd.Series(result, name='cluster')
result = result.aggregate(['value_counts'])
print(result)
