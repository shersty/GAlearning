"""
@Time    : 2020/6/8
@Author  : Suranyi
@System  : MacOS 10.15.3
@Contact : suranyi.sysu@gamil.com
@Version : Python 3.7.4 (default, Aug 13 2019, 15:17:50)
@Describe: 模拟退火算法
"""
import math
import random


class SimulatedAnnealing(object):
    def __init__(self, function, testFunction, F = 800, trueValueNum=5, falseValueNum=5, T=1e8, cool=0.9):
        self.function = function
        self.testFunction = testFunction
        self.F = F
        self.trueValueNum = trueValueNum
        self.falseValueNum = falseValueNum
        self.T = T
        self.cool = cool

    def run(self):
        # 随机的初始解
        vec = [True] * self.trueValueNum + [False] * self.falseValueNum
        random.shuffle(vec)
        while self.testFunction(vec, upperBound=self.F):
            vec = [True] * self.trueValueNum + [False] * self.falseValueNum
            random.shuffle(vec)
        count = 0

        while self.T > 1e-8:
            count += 1
            # 随机选择两个维度
            indexTuple = random.sample(range(self.falseValueNum + self.trueValueNum), 2)
            minIndex = min(indexTuple)
            maxIndex = max(indexTuple)

            # 创建一个代表解的新列表，逆序
            vec_copy = vec.copy()
            vec_copy[minIndex:maxIndex + 1] = reversed(vec_copy[minIndex:maxIndex + 1])

            # 判断这种改变是否合法
            while self.testFunction(vec_copy, upperBound=self.F):
                indexTuple = random.sample(range(self.falseValueNum + self.trueValueNum), 2)
                minIndex = min(indexTuple)
                maxIndex = max(indexTuple)
                vec_copy = vec.copy()
                vec_copy[minIndex:maxIndex + 1] = reversed(vec_copy[minIndex:maxIndex + 1])

            # 计算成本
            e_origin = self.function(vec)
            e_copy = self.function(vec_copy)

            # 判断是否为更优解
            if e_copy < e_origin or random.random() < pow(math.e, -(e_copy - e_origin) / self.T):
                vec = vec_copy.copy()

            # 温度下降
            self.T = self.T * self.cool
            # print(f"This is NO.{count} iteration, the optimal solution for {vec}, f(x) = {self.function(vec)}")
        return vec


class GeneticAlgorithm(object):
    def __init__(self):
        pass