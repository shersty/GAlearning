"""
@Time    : 2020/6/8
@Author  : Suranyi
@System  : MacOS 10.15.3
@Contact : suranyi.sysu@gamil.com
@Version : Python 3.7.4 (default, Aug 13 2019, 15:17:50)
@Describe: 
"""
from Utils import *
# import gurobi


class BoundedRationalChoiceBehaviorModel(object):
    # 有限理性选择行为模型
    def __init__(self, function, gamma=gamma, **kwargs):
        self.optimizeFunction = function
        self.gamma = gamma
        self.kwargs = kwargs

    # 目标函数 公式五
    def fitness(self, vec):
        # 小区 i 居民到避难所 j 避难的概率  公式三
        pij = [[exp(self.gamma * U[i][j]) * vec[j] / (sum(exp(self.gamma * U[i][k]) * vec[k] for k in range(len(JPosition))) + exp(self.gamma * Ui[i])) for j in range(len(JPosition))] for i in range(len(IPosition))]
        # 小区 i 居民选择不避难的概率  公式四
        pi = [exp(self.gamma * Ui[i]) / (sum(exp(self.gamma * U[i][k]) * vec[k] for k in range(len(JPosition))) + exp(self.gamma * Ui[i])) for i in range(len(IPosition))]
        # 避难所j未被服务居民数量  公式六
        betaj = [max(0, sum(alphai[i] * pij[i][j] for i in range(len(IPosition))) - cj[j]) for j in range(len(JPosition))]
        return sum(alphai[i] * pi[i] for i in range(len(IPosition))) + sum(betaj[j] for j in range(len(JPosition)))

    def run(self):
        vec = self.optimizeFunction(self.fitness, TestFunction, **self.kwargs).run()  # 求得的近似最优解
        pij = [[exp(self.gamma * U[i][j]) * vec[j] / (sum(exp(self.gamma * U[i][k]) * vec[k] for k in range(len(JPosition))) + exp(self.gamma * Ui[i])) for j in range(len(JPosition))] for i in range(len(IPosition))]
        return [vec, [[pij[i][j] * alphai[i] for j in range(len(JPosition))] for i in range(len(IPosition))], self.fitness(vec)]


class SimpleModel(object):
    # 简单模型
    def __init__(self, function):
        self.optimizeFunction = function

    # 目标函数
    def fitness(self, vec):
        z1 = [sum(d[i][j] for i in range(len(IPosition))) for j in range(len(JPosition))]


class UtilityOptimalSelectionBehaviorModel(object):
    # 效用最优选择行为
    def __init__(self, function, *args, **kwargs):
        self.optimizeFunction = function
        self.args = args
        self.kwargs = kwargs

    def fitness(self, vec):
        xi = [1 if Ui[i] >= max(U[i][j] * vec[j] for j in range(len(JPosition))) else 0 for i in range(len(IPosition))]
        xij = [[1 if ((U[i][j] == max(U[i][j] * vec[j] for j in range(len(JPosition))) and (U[i][j] > Ui[i]))) else 0 for j in range(len(JPosition))] for i in range(len(IPosition))]

        # 小区 i 居民到避难所 j 避难的概率
        betaj = [max(0, sum(alphai[i] * xij[i][j] for i in range(len(IPosition))) - cj[j]) for j in range(len(JPosition))]
        return sum(alphai[i] * xi[i] for i in range(len(IPosition))) + sum(betaj[j] for j in range(len(JPosition)))

    def run(self):
        vec = self.optimizeFunction(self.fitness, TestFunction, *self.args, **self.kwargs).run()
        xij = [[1 if ((U[i][j] == max(U[i][j] * vec[j] for j in range(len(JPosition))) and (U[i][j] > Ui[i]))) else 0 for j in range(len(JPosition))] for i in range(len(IPosition))]
        return [vec, xij, self.fitness(vec)]


class MedianPBasedOnSystemOptimality(object):
    # 系统最优原则的P 中值，采用 gurobi 求解器

    def run(self):
        Model = gurobi.Model()

        # 添加变量
        z = Model.addVars(len(IPosition), len(JPosition))
        y = Model.addVars(len(JPosition), vtype=gurobi.GRB.BINARY)

        # 添加目标
        Model.setObjective(sum(alphai) - sum(alphai[i] * z[i, j] for i in range(len(IPosition)) for j in range(len(JPosition))), sense=gurobi.GRB.MINIMIZE)

        # 添加约束
        Model.addConstr(sum(y[j] for j in range(len(JPosition))) <= p)
        Model.addConstr(sum(y[j] * fj[j] for j in range(len(JPosition))) <= F)
        Model.addConstrs(sum(z[i, j] for j in range(len(JPosition))) <= 1 for i in range(len(IPosition)))
        Model.addConstrs(sum(alphai[i] * z[i, j] for i in range(len(IPosition))) <= cj[j] * y[j] for j in range(len(JPosition)))

        Model.Params.LogToConsole = False
        Model.optimize()
        return [[y[j].X for j in range(len(JPosition))], [[z[i, j].X for i in range(len(IPosition))] for j in range(len(JPosition))], Model.objVal]
