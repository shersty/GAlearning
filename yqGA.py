import numpy as np
import geatpy as ea
from utils.UnDirectedGraph import UnDirectedGraph as udGra
import sys


class YQProblem(ea.Problem):
    def __init__(self):
        name = 'YQProblem'
        M = 1
        maxormins = [-1]
        Dim = 4  # 决策变量维数
        varTypes = [0, 1, 1, 0]  # 决策变量类型，0--连续  1--离散
        lb = [0, 0, 0, 0]  # 决策变量下界
        ub = [1, 1, 1, 1]  # 决策变量上界
        lbin = [1] * Dim
        ubin = [1] * Dim

        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, population):
        y_q = population.Phen[:, [0]]
        a_hk = population.Phen[:, [1]]
        b_qh = population.Phen[:, [2]]
        v_h = population.Phen[:, [3]]
        Q = []
        H = []
        K = []
        f = 0
        for q in Q:
            f = f + getReqestAmount(q) * y_q

        sumBqhVh = 0
        for h in H:
            sumBqhVh = sumBqhVh + b_qh * v_h

        limit1 = sumBqhVh - y_q
        limit2 = a_hk * x_k - v_h


def getReqestAmount(self, q):
    # 根据空间引力模型求给定路径上的过路需求量
    return 0


# 获取充电站组合
def getH():
    odGraph = getODGraph()
    for origin in range(25):
        for destination in range(25):
            minCostOD = odGraph.dijkstra(origin + 1)[0][destination + 1]
            parentNode = odGraph.dijkstra(origin + 1)[1][destination + 1]
            parentNodes = [destination + 1]
            if parentNode is not None:
                parentNodes.append(parentNode)
            # print(origin + 1, " to ", destination + 1, "==>", minCostOD)
            while (parentNode is not None) & (origin + 1 != parentNode):
                parentNode = odGraph.dijkstra(origin + 1)[1][parentNode]
                parentNodes.append(parentNode)
            parentNodes.reverse()
            print(parentNodes)


# 生成OD网络图
def getODGraph():
    UG = udGra()
    UG.add_edge(1, 2, 4)
    UG.add_edge(1, 5, 5)
    UG.add_edge(2, 3, 3)
    UG.add_edge(2, 4, 4)
    UG.add_edge(3, 4, 4)
    UG.add_edge(3, 9, 4)
    UG.add_edge(4, 5, 3)
    UG.add_edge(4, 7, 5)
    UG.add_edge(4, 8, 5)
    UG.add_edge(4, 9, 7)
    UG.add_edge(5, 6, 5)
    UG.add_edge(5, 7, 5)
    UG.add_edge(6, 7, 3)
    UG.add_edge(7, 8, 3)
    UG.add_edge(7, 11, 8)
    UG.add_edge(7, 12, 9)
    UG.add_edge(8, 9, 6)
    UG.add_edge(8, 10, 6)
    UG.add_edge(8, 11, 7)
    UG.add_edge(9, 10, 6)
    UG.add_edge(10, 13, 6)
    UG.add_edge(10, 14, 3)
    UG.add_edge(11, 12, 2)
    UG.add_edge(11, 13, 3)
    UG.add_edge(11, 16, 7)
    UG.add_edge(12, 15, 4)
    UG.add_edge(12, 16, 4)
    UG.add_edge(13, 14, 7)
    UG.add_edge(13, 19, 4)
    UG.add_edge(14, 19, 7)
    UG.add_edge(14, 21, 2)
    UG.add_edge(14, 22, 4)
    UG.add_edge(15, 16, 4)
    UG.add_edge(16, 17, 4)
    UG.add_edge(17, 18, 3)
    UG.add_edge(17, 19, 3)
    UG.add_edge(19, 20, 3)
    UG.add_edge(20, 21, 2)
    UG.add_edge(22, 23, 3)
    UG.add_edge(23, 24, 3)
    UG.add_edge(24, 25, 8)
    return UG


if __name__ == '__main__':
    getH()
