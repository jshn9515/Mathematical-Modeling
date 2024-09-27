import pandas as pd
import statsmodels.api as sm

df = pd.read_excel('问题2-山东省农业气象数据汇总表.xlsx', index_col=0)
X = df.iloc[:, :13]
X = sm.add_constant(X)
with open('问题3-GLM结果统计表.html', 'w', encoding='gbk') as fp:
    for i in range(13, 17):
        y = df.iloc[:, i]
        Mdl = sm.GLM(y, X)
        result = Mdl.fit()
        summary = result.summary()
        html = summary.as_html()
        fp.writelines('-' * 80)
        fp.write(html)
