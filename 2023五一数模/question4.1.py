import numpy as np
import pandas as pd
import networkx as nx
from itertools import islice


def k_shortest_paths_length(G: nx.Graph | nx.DiGraph, source: str, target: str, k: int):
    paths = list(islice(nx.shortest_simple_paths(G, source, target), k))
    for path in paths:
        distance = 0
        for dist in range(len(path) - 1):
            distance += G[path[dist]][path[dist + 1]]['weight']
        yield distance


def is_symmetric(matrix: np.ndarray | pd.DataFrame) -> bool:
    A = np.array(matrix)
    B = np.transpose(A)
    if np.allclose(A, B):
        return True
    return False


def calculate_price(cargo: int, cost: list) -> float:
    count = cargo // 200
    if cargo % 200 == 0:
        count -= 1
    price = cost[count] * (1 + ((cargo - 200 * count) / 200) ** 3) + sum(cost[:count]) * 2
    return price


df1 = pd.read_excel('附件/附件2(Attachment 2)2023-51MCM-Problem B.xlsx', index_col=0)
df2 = pd.read_excel('附件/附件3(Attachment 3)2023-51MCM-Problem B.xlsx')
time_range = pd.date_range('2023-04-23', '2023-04-27', freq='D').strftime('%Y-%m-%d')
city_start = df2['起点 (Start)'].unique()
city_end = df2['终点 (End)'].unique()
adjacency_matrix = pd.DataFrame(index=city_start, columns=city_end)
for i in range(df2.shape[0]):
    adjacency_matrix.loc[df2.iloc[i, 0], df2.iloc[i, 1]] = df2.iloc[i, 2]
adjacency_matrix = adjacency_matrix.astype(float)
adjacency_matrix.fillna(0, inplace=True)
G = nx.DiGraph(adjacency_matrix)
result = {}
for time in time_range:
    price = {}
    df_temp: pd.DataFrame = df1[df1.index == time]
    for row in df_temp.itertuples(index=False):
        cost = []
        city1, city2, cargo = row
        for distance in k_shortest_paths_length(G, city1, city2, 5):
            cost.append(round(distance, 4))
        cost.sort()
        price[city1 + city2] = round(calculate_price(cargo, cost), 4)
    result[time] = price
result = pd.DataFrame.from_dict(result, orient='columns')
result.fillna(0, inplace=True)
result.sort_index(inplace=True)
# result.to_excel('单条线路运费.xlsx', index_label='快递运输路线 (Express delivery route)')
total_price = result.sum()
# total_price.to_excel('总运费.xlsx', index_label='日期(年/月/日) (Date Y/M/D)', header=['总运费 (Total freight)'])
