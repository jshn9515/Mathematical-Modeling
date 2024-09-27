import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA

df = pd.read_excel('问题1-蘑菇原始数据.xlsx')
encoder = LabelEncoder()
data = df.values
for col in range(data.shape[1]):
    data[:, col] = encoder.fit_transform(data[:, col])
Mdl = PCA()
pca = Mdl.fit_transform(df)
print(pca)
