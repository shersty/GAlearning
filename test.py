import numpy as np
from geatpy import crtpc

# help(crtpc)
Nind = 4  # 种群规模
Encoding = 'RI'  # 实整数编码
FieldDR = np.array([[-3.1, -2, 0, 3],  # 下界
                    [4.2, 2, 1, 5],  # 上界
                    [0, 0, 1, 1]])  # 0-连续  1-离散
Chrom = crtpc(Encoding, Nind, FieldDR)
print(Chrom)

Nind = 4
Encoding = 'BG'
FieldD = np.array([[3, 2],  # 各决策变量编码后所占二进制位数--与决策变量范围以及精度相关，染色体长度为求和所得
                   [0, 0],  # 下界
                   [7, 3],  # 上界
                   [0, 0],  # 编码方式 0--二进制  1--格雷码
                   [0, 0],  # 是否采用对数刻度 0--算术刻度 1--对数刻度
                   [1, 1],  # 范围是否包含下界 0--不含 1--包含
                   [1, 1],  # 范围是否包含上界 0--不含 1--包含
                   [0, 0]])  # 0--连续 1--离散
Chrom = crtpc(Encoding, Nind, FieldD)
print(Chrom)

