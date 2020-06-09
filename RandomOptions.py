import random
import numpy as np
import matplotlib.pyplot as plt


def generateIPosition():
    IPosition = []
    IPositions = []
    JPosition = []
    JPositions = []
    # 生成小区位置
    num = 0
    while num < 30:
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        position = np.array([x, y])
        # 第一次进入
        if len(IPosition) == 0:
            IPosition.append(position)
            IPositions.append(tuple(position))
            continue
        count = 0
        # 之后随机的位置需要进行比较 判断距离不能过近
        for p in IPosition:
            print(p)
            # 如果距离小于 N ，重新选点
            if np.linalg.norm(p - position) < 10:
                print("*")
                break
            count = count + 1
            # 如果比较完了所有的点，将当前随机到的点添加到列表中
            if count == len(IPosition):
                print(count)
                IPosition.append(position)
                IPositions.append(tuple(position))
                num = num + 1
                break
    print("IPosition =", IPositions)
    # 生成避难点位置
    num = 0
    while num < 10:
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        position = np.array([x, y])
        if len(JPosition) == 0:
            # 遍历小区列表
            for i in IPosition:
                # 如果随机产生的点距离和小区距离小于5,跳出循环下一次
                if np.linalg.norm(i - position) < 10:
                    break
                JPosition.append(position)
        else:
            # 遍历小区列表
            count = 0
            for i in IPosition + JPosition:
                # 如果随机产生的点和小区距离小于5,跳出循环下一次
                if np.linalg.norm(i - position) < 10:
                    break
                count = count + 1
                if count == len(IPosition + JPosition):
                    JPosition.append(position)
                    JPositions.append(tuple(position))
                    num = num + 1
                    break
    print("JPosition =", JPositions)

    plt.title('test')
    xi = []
    yi = []
    for point in IPosition:
        xi.append(point[0])
        yi.append(point[1])
    xj = []
    yj = []
    for point in JPosition:
        xj.append(point[0])
        yj.append(point[1])
    plt.plot(xi, yi, 'ob')
    plt.plot(xj, yj, 'vr')
    plt.show()


# 生成小区人口
def generateAlphai():
    alphai = []
    for num in range(30):
        alphai.append(round(random.uniform(0, 10), 1))
    print("alphai = ", alphai)

    print("#people =", sum(alphai))

    cj = []
    fj = []
    for num in range(10):
        cj.append(round((random.uniform(10, 30)), 1))
    print("#", sum(cj))
    for c in cj:
        fj.append(round(c * 5, 1))
    print("cj =", cj)
    print("fj =", fj)
    print("#", sum(fj))


if __name__ == '__main__':
    generateIPosition()
    generateAlphai()
