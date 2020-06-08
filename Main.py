"""
@Time    : 2020/6/8
@Author  : Suranyi
@System  : MacOS 10.15.3
@Contact : suranyi.sysu@gamil.com
@Version : Python 3.7.4 (default, Aug 13 2019, 15:17:50)
@Describe: 
"""

from Optimizes import SimulatedAnnealing
from Models import *

## 表 6
# the optimal solution for [True, False, True, False, False, False, True, True, False, True], f(x) = 17.196996671175803
vec = BoundedRationalChoiceBehaviorModel(SimulatedAnnealing).run()
print(f"模型 P1: {[index + 1 for index, value in enumerate(vec[0]) if value > 0]}, 目标函数值: {vec[2]}")
for i in range(len(vec[1])):
    print(i + 1, end="\t")
    for index in [index for index, value in enumerate(vec[0]) if value > 0]:
        print(vec[1][i][index], end="\t")
    print()

# the optimal solution for [False, True, True, False, False, True, True, False, True, False], f(x) = 20.599999999999998
vec = UtilityOptimalSelectionBehaviorModel(SimulatedAnnealing).run()
print(f"模型 P2 目标函数值: {vec[2]}")
print("备选点 ID\t小区 ID")
for i in range(len(vec[0])):
    if (vec[0][i] > 0):
        print(f"{i + 1}\t\t{[j + 1 for j in range(len(vec[1])) if vec[1][j][i] > 0]}")

# 该模型有多个最优解，返回了 [1, 3, 7, 8, 10]，需要有 gurobi 求解器
# vec = MedianPBasedOnSystemOptimality().run()
# print(f"模型 P3: 目标函数值: {vec[2]}")
# print("备选点 ID\t小区 ID")
# for i in range(len(vec[0])):
#     if (vec[0][i] > 0):
#         print(f"{i + 1}\t\t{[j + 1 for j in range(len(vec[1][0])) if vec[1][i][j] > 0]}")

# 表 8
for gamm in range(11):
    vec = BoundedRationalChoiceBehaviorModel(SimulatedAnnealing, gamm).run()
    print(f"模型 P1: 理性程度： { gamm }, 选址结果： {[index + 1 for index, value in enumerate(vec[0]) if value > 0]}, 目标函数值: {vec[2]}")

# 表 9，pv = 9 无解
for pv in range(1, 9):
    vec = BoundedRationalChoiceBehaviorModel(SimulatedAnnealing, trueValueNum=pv, falseValueNum=10 - pv).run()
    print(f"模型 P1: {[index + 1 for index, value in enumerate(vec[0]) if value > 0]}, 目标函数值: {vec[2]}")

# 表 10 手动修改 Options 文件中的参数值 [291, 292, 300, 400, 500, 600, 700, 800, 898.5, 900.0]
