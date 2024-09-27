import json5
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB

start = 1
end = 27
s = [1,  1,  2,  3,  3,  3,  4,  4,  4,  5,  5,  6,  6,  6,  7,  7,  8,  8,  9,  9,  9,  9,  9,  9,  10, 10, 10,
     11, 11, 12, 12, 13, 13, 14, 14, 15, 16, 16, 17, 17, 18, 18, 19, 20, 21, 21, 21, 22, 23, 23, 24, 24, 25, 26]
t = [2,  25, 3,  2,  4,  25, 5,  24, 25, 6,  24, 7,  23, 24, 8,  22, 9,  22, 10, 15, 16, 17, 21, 22, 11, 13, 15,
     12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 18, 18, 21, 19, 20, 20, 21, 22, 23, 27, 23, 24, 26, 25, 26, 26, 27]
s = np.array(s)
t = np.array(t)
G1: nx.Graph = nx.from_edgelist(zip(s, t))
for i in range(1, 28):
    G1.add_edge(i, i)
G2: nx.DiGraph = nx.to_directed(G1)

plt.figure(3)
nx.draw_kamada_kawai(G1, with_labels=True)

days = list(range(1, 31))
weather = [None, 2, 2, 1, 3, 1, 2, 3, 1, 2, 2, 3, 2, 1, 2, 2, 2, 3, 3, 2, 2, 1, 1, 2, 1, 3, 2, 1, 1, 2, 2]
weather_water = [None, 8, 8, 5, 10, 5, 8, 10, 5, 8, 8, 10, 8, 5, 8, 8, 8, 10, 10, 8, 8, 5, 5, 8, 5, 10, 8, 5, 5, 8, 8]
weather_food = [None, 6, 6, 7, 10, 7, 6, 10, 7, 6, 6, 10, 6, 7, 6, 6, 6, 10, 10, 6, 6, 7, 7, 6, 7, 10, 6, 7, 7, 6, 6]

model = gp.Model('question1')
x = model.addVars(G2.edges, days, vtype=GRB.BINARY, name='x')
money = model.addVars(range(31), vtype=GRB.INTEGER, lb=0, name='money')
water = model.addVars(range(31), vtype=GRB.INTEGER, lb=0, name='water')
food = model.addVars(range(31), vtype=GRB.INTEGER, lb=0, name='food')
z1 = model.addVars(days, vtype=GRB.BINARY, name='stop_or_not')
z2 = model.addVars(days, vtype=GRB.BINARY, name='mining_or_not')
z3 = model.addVars(days, vtype=GRB.BINARY, name='trade_or_not')
b = model.addVars(days, vtype=GRB.INTEGER, name='factor')
village_water = model.addVars(days, vtype=GRB.INTEGER, lb=0, name='village_water')
village_food = model.addVars(days, vtype=GRB.INTEGER, lb=0, name='village_food')
mining_resource = model.addVars(days, vtype=GRB.INTEGER, lb=0, name='mining_resource')

cost = 5 * water[0] + 10 * food[0]
weight = 3 * water[0] + 2 * food[0]
model.addConstr(money[0] == 10000)
model.addConstr(5 * water[0] + 10 * food[0] <= money[0])
model.addConstrs(3 * water[k] + 2 * food[k] <= 1200 for k in days)
model.addConstrs(gp.quicksum(x[i, j, k] for i, j in G2.edges) == 1 for k in days)
model.addConstr(gp.quicksum(x[start, j, 1] for j in G2.successors(start)) == 1)
model.addConstr(gp.quicksum(x[i, end, k] for i in G2.predecessors(end) if i != end for k in days) == 1)
model.addConstrs(x[end, j, k] == 0 for j in G2.successors(end) for k in days)
for k in days[:-1]:
    for n in G2.nodes:
        if n != start and n != end:
            model.addConstr(
                gp.quicksum(x[i, n, k] for i in G2.predecessors(n)) == gp.quicksum(x[n, j, k + 1] for j in G2.successors(n))
            )
    model.addConstr(x[27, 27, k + 1] == gp.quicksum(x[n, end, k] for n in G2.predecessors(end)))
for k in days:
    model.addConstr(z1[k] == gp.quicksum(x[n, n, k] for n in G2.nodes))
    model.addConstr(weather[k] - gp.quicksum(x[n, n, k] for n in G2.nodes) <= 2)
    model.addGenConstrIndicator(z1[k], True, b[k] == 1, name='stop')
    model.addGenConstrIndicator(z1[k], False, b[k] == 2, name='move')
    model.addGenConstrIndicator(z2[k], True, b[k] == 3, name='mining')
    model.addGenConstrIndicator(x[end, end, k], True, b[k] == 0, name='at_the_end')
    model.addGenConstrIndicator(x[12, 12, k], True, z2[i] == 1, name='place_to_mining')
    model.addConstr(z3[k] <= gp.quicksum(x[n, 15, k] for n in G2.predecessors(15)), name='pass_through_villege')
    model.addGenConstrIndicator(z3[k], True, village_water[k] >= 0, name='can_buy_water')
    model.addGenConstrIndicator(z3[k], False, village_food[k] == 0, name='cannot_buy_food')
    model.addGenConstrIndicator(z3[k], True, village_food[k] >= 0, name='can_buy_food')
    model.addGenConstrIndicator(z3[k], False, village_water[k] == 0, name='cannot_buy_water')
    model.addConstr(mining_resource[k] == 1000 * z2[k])
    model.addConstr(
        10 * village_water[k] + 20 * village_food[k] <= 10000 - cost - 
        gp.quicksum(10 * village_water[i] + 20 * village_food[i] - mining_resource[i] for i in days[:k])
    )
    model.addConstr(
        3 * village_water[k] + 2 * village_food[k] <= 1200 - weight - 
        gp.quicksum(
            3 * village_water[i] + 2 * village_food[i] - 3 * weather_water[k] * b[i] - 2 * weather_food[k] * b[i] for i in days[:k]
        )
    )
    model.addConstr(
        money[k] == 10000 + mining_resource[k] - cost - 
        gp.quicksum(10 * village_water[i] + 20 * village_food[i] - mining_resource[i] for i in days[:k])
    )
    model.addConstr(
        water[k] == water[0] - gp.quicksum(weather_water[k] * b[i] - 3 * village_water[i] for i in days[:k]) - weather_water[k] * b[k]
    )
    model.addConstr(
        food[k] == food[0] - gp.quicksum(weather_food[k] * b[i] - 2 * village_food[i] for i in days[:k]) - weather_food[k] * b[k]
    )

model.setObjective(money[30] + 2.5 * water[30] + 5 * food[30], GRB.MINIMIZE)

model.optimize()
result = model.getJSONSolution()
with open('result.json', 'w') as fp:
    json5.dump(result, fp)

route = [start]
route.extend([j for i, j in G2.edges for k in days if x[i, j, k].X > 0.5])
result = pd.DataFrame({
    '日期': list(range(31)),
    '所在区域': route,
    '剩余资金数': [money[i].X for i in range(31)],
    '剩余水量': [water[i].X for i in range(31)],
    '剩余食物量': [food[i].X for i in range(31)],
})
result.set_index('日期', inplace=True)
result.to_excel('result.xlsx')
