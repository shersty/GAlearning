import geatpy as ga  # 解遗传算法的库
from pymprog import *  # 解运输问题的库
import numpy as np
import xlrd


# -------------------解码函数---------------------------
def decode(Y, A, B, m):
    # step1
    List1 = np.multiply(np.array(Y), np.array(A))  # 计算 y*a

    sum1 = 0  # 再把他们累加起来
    for i in List1:
        sum1 += i

    sum2 = 0
    for j in B:
        sum2 += j

    # step2
    while sum1 < sum2:
        k = np.random.randint(0, m)
        if Y[k] == 0:
            sum1 += A[k]
            Y[k] = 1
        else:
            k = np.random.randint(1, m + 1)
            continue
    # else:

    # print("算法终止")

    return Y


# -----------------------适值函数-------------------------------
# 固定成本函数
def Fixed_cost(List2):
    fixed_cost = 0  # 再进行累加计算    计算建厂的固定成本
    for i in List2:
        fixed_cost += i
    return fixed_cost


# 运输成本函数
def report(Y_decode, A, B):  # 返回(产地,销地):运价；产地:产量； 销地:销量
    # 把目标函数简化成产大于销的运输问题
    a = ("A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10")  # 工厂（产地）
    b = ("B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10",
         "B11", "B12", "B13", "B14", "B15", "B16", "B17", "B18", "B19", "B20", "B21")  # 需求地（销地）
    datas = dict()  # 定义一个空字典 (产地,销地):运价
    datac = dict()  # 定义一个空字典   产地:产量
    datax = dict()  # 定义一个空字典   销地:销量
    List3 = np.multiply(np.array(Y_decode), np.array(A))  # 计算 y*a    产量

    # （产地，销地）：运价
    Data = xlrd.open_workbook('单位运输费用.xlsx')  # 读取Excel运价列表
    table = Data.sheets()[0]  # 读取Excel列表的sheet1
    for i in range(0, 10):  # 先从十行里面拿出一行来
        x = np.array(table.row_values(i))
        for j in range(0, 21):  # 再从21列中取一列
            data = x[j]
            datas[a[i], b[j]] = data  # (产地,销地):运价

    # 产地：产量
    y = List3

    for i in range(0, 10):
        datac[a[i]] = y[i]  # 产地:产量

    # 销地：销量
    for j in range(0, 21):
        datax[b[j]] = B[j]  # 销地:销量
    return (datas, datac, datax)


def Transport_cost(datas, datac, datax):
    a = ("A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10")  # 工厂（产地）
    b = ("B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10",
         "B11", "B12", "B13", "B14", "B15", "B16", "B17", "B18", "B19", "B20", "B21")  # 需求地（销地）
    # 开始模型计算
    X = np.zeros((10, 21))   # 生成10行21列的0矩阵
    cost = 0.0
    begin('Transport')
    x = var('x', datas.keys())  # 调运方案
    minimize(sum(datas[i, j] * x[i, j] for (i, j) in datas.keys()), 'Cost')  # 总运费最少
    for i in datac.keys():  # 产地产量约束
        sum(x[i, j] for j in datax.keys()) == datac[i]
    for j in datax.keys():  # 销地销量约束
        sum(x[i, j] for i in datac.keys()) == datax[j]
    solve()

    for (i, j) in datas.keys():
        # print('x[i, j].primal',x[i, j].primal)
        if x[i, j].primal > 0 and datas[i, j] != 0:
            # print("产地:%s -> 销地:%s 运输量:%-2d 运价:%2d" % (i, j, int(x[i, j].primal), int(datas[i, j])))
            X[a.index(i)][b.index(j)] = int(x[i, j].primal)
    cost = int(vobj())
    # print("X", X)
    # print("总费用:%d" % int(vobj()))
    end()
    return (X, cost)


# -----------------------主函数开始-------------------------------------
def main():
    # 需求点的需求量
    B = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0]

    # 工厂容量（生产能力）
    A = [30, 40, 50, 55, 45, 48, 36, 50, 60, 35]

    # 各待选工厂的固定费用
    D = [65, 50, 40, 30, 20, 50, 45, 30, 35, 25]

    # 从待选工厂到需求点的单位运输费用
    Data = xlrd.open_workbook('单位运输费用.xlsx')
    table = Data.sheets()[0]

    Y = []  # 定义变量码
    Y_decode = []  # 定义解码生成的变量码
    m = 10  # 工厂个数
    T = 100  # 迭代次数
    decode_after_chrom2 = np.zeros((60, 10))    # 存储60条Y_decode
    datas = dict()  # 定义一个空字典 (产地,销地):运价
    datac = dict()  # 定义一个空字典   产地:产量
    datax = dict()  # 定义一个空字典   销地:销量
    fixed_cost = 0.0  # 初始固定成本
    X = np.zeros((10, 21))  # 运量矩阵
    transport_cost = 0.0  # 初始运输费用
    cost = 0.0  # 初始总费用

    best_y = np.zeros((1, 10))  # 所有代中的最优选址方案
    min_t = 0  # 最优的方案出现的代数
    all_min_cost = 1000  # 所有代中最小总费用
    all_min_X = np.zeros((10, 21))  # 所有代中最小总费用的运量矩阵
    FitnV = np.zeros((1, 60))  # 适应度列表
    NewChrlx = []  # 轮盘赌存储位置
    New_chrom1 = np.zeros((60, 10))
    New_chrom2 = np.zeros((60, 10))

    # ---------------------遗传编码---------------------------

    # 生成附加码
    chrom1 = ga.crtpp(60, 10, 10)   # 种群大小，染色体长度，种群最大元素
    print(chrom1)

    # 生成变量码
    FieldDR = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
    chrom2 = ga.crtip(60, FieldDR)   # 种群大小，上界下界区域描述器
    print(chrom2)
    add_code = np.zeros((1, 10))  # 定义父代单行附加码
    new_add_code = np.zeros((1, 10))  # 定义子代单行附加码
    variable_code = np.zeros((1, 10))  # 定义父代单行变量码
    new_variable_code = np.zeros((1, 10))  # 定义子代单行变量码
    index_v = 0  # 定义初始索引值
    begin_New_chrom2 = np.zeros((60, 10))  # 定义经过交叉后的新的变量码种群
    again_New_chrom1 = np.zeros((60, 10))  # 经过变异后的附加码种群
    # tem_list = []
    a = 0
    for t in np.arange(0, T):
        min_cost = 1000  # 初始最小总费用
        min_X = np.zeros((10, 21))  # 初始最小总费用的运量矩阵
        min_i = 400  # 每一代中最小的运价在种群对应的位置
        better_y = np.zeros((1, 10))  # 每一代中的最有选址方案
        print("==========================第%d代种群======================" % t)

        for i in np.arange(0, 60):
            # print("第%d个染色体" % i)
            Y = chrom2[i]
            # print("-------------%d-----------------" % i)
            # print("Y",Y)
            Y_decode = np.array(decode(Y, A, B, m))
            decode_after_chrom2[i] = Y_decode
            List2 = np.multiply(np.array(D), np.array(Y_decode))  # 计算 d*y
            fixed_cost = Fixed_cost(List2)
            print("fixed_cost", fixed_cost)
            (datas, datac, datax) = report(Y_decode, A, B)
            (X, transport_cost) = Transport_cost(datas, datac, datax)
            cost = fixed_cost + transport_cost
            print('第%d个染色体的cost' % i, cost)
            FitnV[0][i] = 1 / cost
            if cost < min_cost:
                min_cost = cost
                min_X = X
                min_i = i
                better_y = Y_decode
            # print("第%d代种群中最小的cost"%t, min_cost)
            # print("最优运输方案", min_X)
            # print('对应的位置', min_i)
        NewChrlx = ga.rws(np.array(FitnV).T, 59)  # 轮盘赌
        # print(NewChrlx)
        for i in NewChrlx:
            New_chrom1[i] = chrom1[i]
            New_chrom2[i] = decode_after_chrom2[i]
            for j in range(0, 60):  # 把最大的适值得到染色体拿到新的种群中
                if j not in NewChrlx:
                    New_chrom1[j] = chrom1[j]
                    New_chrom2[j] = decode_after_chrom2[j]

        # 遗传操作
        Pc = 0.6  # 交叉概率
        Pm = 0.1  # 变异概率
        New_chrom1 = ga.xovpm(New_chrom1, 0.6)
        # print("交叉后的附加码New_chrom1",New_chrom1)
        # print("chrom1",chrom1)
        for change_1 in np.arange(0, 60):
            # print('------------修改chrom2第%d次-----------'%change_1)
            new_add_code = New_chrom1[change_1]
            add_code = chrom1[change_1]
            # print(type(add_code))
            variable_code = New_chrom2[change_1]
            for change_2 in np.arange(0, 10):
                index_v = add_code.tolist().index(new_add_code[change_2])
                # print("index_v",index_v)
                new_variable_code[0, change_2] = variable_code[index_v]
            begin_New_chrom2[change_1] = new_variable_code
            # print("begin_New_chrom2[change_1]",begin_New_chrom2[change_1])
            new_variable_code = np.zeros((1, 10))
        # print("交叉后的变量码begin_New_chrom2",begin_New_chrom2)
        # 变异操作
        ret = np.random.random()
        if ret > Pm:
            for mutation_v in np.arange(0, 60):
                new_add_code = New_chrom1[mutation_v]
                # print('未翻转的附加码new_add_code',new_add_code)
                random_1 = np.random.randint(0, 10)
                random_2 = np.random.randint(0, 10)
                a = np.abs(random_1 - random_2)
                tem_list = np.zeros(a + 1)
                if a != 0:
                    if random_2 > random_1:
                        for i, k in zip(np.arange(0, np.abs(random_2 - random_1) + 1), np.arange(random_1, random_2 + 1)):
                            tem_list[i] = new_add_code[k]
                        # print("未翻转的单行tem_list",tem_list)
                        # print("未翻转的tem_list类型",type(tem_list))
                        tem_list = tem_list.tolist()
                        # print("转换为列表的tem_list", tem_list)
                        tem_list.reverse()
                        # print("翻转后的tem_list",tem_list)
                        for i, k in zip(np.arange(0, np.abs(random_2 - random_1) + 1).tolist(),
                                        np.arange(random_1, random_2 + 1).tolist()):
                            new_add_code[k] = tem_list[i]
                        # print("翻转后的附加码",new_add_code)
                        again_New_chrom1[mutation_v] = new_add_code

                    else:
                        for i, k in zip(np.arange(0, np.abs(random_2 - random_1) + 1), np.arange(random_2, random_1 + 1)):
                            tem_list[i] = new_add_code[k]
                            # print("未翻转的单行tem_list",tem_list)
                        # print("未翻转的tem_list类型",type(tem_list))
                        tem_list = tem_list.tolist()
                        # print("转换为列表的tem_list",tem_list)
                        tem_list.reverse()
                        # print("tem_list",tem_list)
                        for i, k in zip(np.arange(0, np.abs(random_2 - random_1) + 1).tolist(),
                                        np.arange(random_2, random_1 + 1).tolist()):
                            new_add_code[k] = tem_list[i]
                        again_New_chrom1[mutation_v] = new_add_code
                    # print("循环中的again_New_chrom1", again_New_chrom1)
                else:
                    again_New_chrom1[mutation_v] = new_add_code
                    # print("else循环中的again_New_chrom1", again_New_chrom1)
        # print("New_chrom1",New_chrom1)
        # print('变异后的附加码again_New_chrom1',again_New_chrom1)
        chrom1 = again_New_chrom1
        chrom2 = begin_New_chrom2
        print('遗传操作后的chrom2', chrom2)
        print("第%d代种群中最小的cost" % t, min_cost)
        print("最优运输方案", min_X)
        print('对应的位置', min_i)
        if all_min_cost > min_cost:
            all_min_cost = min_cost
            all_min_X = min_X
            best_y = better_y
            min_t = t
    # New_chrom1[60]= chrom1[min_i]
    # New_chrom2[60] = decode_after_chrom2[min_i]
    # print("FitnV",np.array(FitnV).T.shape)
    print("所有代中种群中最小的cost", all_min_cost)
    print("所有代中的最优运输方案", all_min_X)
    print("最优的选址方案", best_y)
    print("最优的选址方案出现在第%d代" % min_t)


if __name__ == "__main__":
    main()