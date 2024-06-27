import numpy as np
import pandas as pd
import networkx as nx
from itertools import islice


def k_shortest_paths(G: nx.Graph | nx.DiGraph, source: str, target: str, k: int, weight=None):
    return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))


def k_shortest_paths_length(G: nx.Graph | nx.DiGraph, source: str, target: str, k: int, weight=None):
    paths = k_shortest_paths(G, source, target, k, weight=weight)
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
city_start = df2['起点 (Start)'].unique()
city_end = df2['终点 (End)'].unique()
adjacency_matrix = pd.DataFrame(index=city_start, columns=city_end)
for i in range(df2.shape[0]):
    adjacency_matrix.loc[df2.iloc[i, 0], df2.iloc[i, 1]] = df2.iloc[i, 2]
adjacency_matrix = adjacency_matrix.astype(float)
adjacency_matrix.fillna(0, inplace=True)
G = nx.DiGraph(adjacency_matrix)
result = {}
city1, city2 = 'G', 'V'
for path in k_shortest_paths(G, city1, city2, 5):
    print(path)
