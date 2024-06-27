import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.multiclass import OutputCodeClassifier
from sklearn.svm import SVC

df1 = pd.read_excel('问题3-铅钡高钾机器学习数据.xlsx', sheet_name='训练数据', usecols='C:Q')  # noqa
df2 = pd.read_excel('问题3-铅钡高钾机器学习数据.xlsx', sheet_name='预测数据', usecols='C:F')  # noqa
df1 = df1.fillna(0)
df2 = df2.fillna(0)
data1 = df1.iloc[0:12, [0, 2, 3, 5, 14]]
data2 = df2.iloc[0:3, :]
data3 = df1.iloc[15:38, [0, 5, 8, 9, 14]]
data4 = df2.iloc[6:11, :]
data4.columns = df2.iloc[5, :]
noise1 = np.random.randn(*data2.shape)
noise2 = np.random.randn(*data4.shape)
Mdl1 = OutputCodeClassifier(SVC())
Mdl2 = OutputCodeClassifier(SVC())
encoder1 = LabelEncoder()
encoder2 = LabelEncoder()
data1['亚类'] = encoder1.fit_transform(data1['亚类'])
data3['亚类'] = encoder2.fit_transform(data3['亚类'])
Mdl1.fit(data1.iloc[:, :-1], data1['亚类'])
Mdl2.fit(data3.iloc[:, :-1], data3['亚类'])
class1 = Mdl1.predict(data2)
class2 = Mdl2.predict(data4)
class1 = encoder1.inverse_transform(class1)
class2 = encoder2.inverse_transform(class2)
print('The first result is: \n', class1)
print('The second result is: \n', class2)
