"""
@Time    : 2020/6/7
@Author  : Suranyi
@System  : MacOS 10.15.3
@Contact : suranyi.sysu@gamil.com
@Version : Python 3.7.4 (default, Aug 13 2019, 15:17:50)
@Describe: 
"""
from math import exp, sqrt
from Options import *


# 定义 Aij 计算式
def getAij(cj_: float, sj: float = 1, di_: float = 1) -> float:
    # 避难所吸引力
    return cj_ * sj / di_


# 定义 Uij 计算式
def getUij(Aij: float, Lambda: float, dij: float) -> float:
    # 避难所 j 对小区 i 居民的效用函数
    return Aij * exp(- Lambda * dij)


# 定义 Ui 计算式
def getUi(Ai: float, Lambda: float, D: float) -> float:
    # 虚拟避难所对小区 i 居民的效用函数
    return Ai * exp(- Lambda * D)


# 使得 cj 无量纲化, 此时转化为 cj'
cj_ = [cj[j] / max(cj) for j in range(len(JPosition))]

# 避难所 j 与小区 i 的距离
d = [[((IPosition[i][0] - JPosition[j][0]) ** 2 + (IPosition[i][1] - JPosition[j][1]) ** 2) ** (1 / 2) for j in
      range(len(JPosition))] for i in range(len(IPosition))]

# 避难所 j 对小区 i 居民的吸引力
sj = [((center[0] - JPosition[j][0]) ** 2 + (center[1] - JPosition[j][1]) ** 2) ** (1 / 2) for j in
      range(len(JPosition))]
di_ = [((center[0] - IPosition[i][0]) ** 2 + (center[1] - IPosition[i][1]) ** 2) ** (1 / 2) for i in
       range(len(IPosition))]
A = [[getAij(cj_[j], sj[j], di_[i]) for j in range(len(JPosition))] for i in range(len(IPosition))]

# 避难所 j 对小区 i 居民的效用
U = [[getUij(A[i][j], Lambda, d[i][j]) for j in range(len(JPosition))] for i in range(len(IPosition))]

# 虚拟避难所对小区 i 居民的吸引力 (吸引力只与人数有关)
Ai = [min([A[i][j] for j in range(len(JPosition))]) for i in range(len(IPosition))]

# 虚拟避难所对小区 i 居民的效用
Ui = [getUi(Ai[i], Lambda, D) for i in range(len(IPosition))]


# 解向量验证函数
def TestFunction(vec: list, upperBound: float = F, fj: list = fj) -> float:
    return sum([fj[j] if vec[j] else 0 for j in range(len(JPosition))]) > upperBound


if __name__ == '__main__':
    pass
