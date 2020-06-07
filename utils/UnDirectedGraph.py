MAXL = 99999
class UnDirectedGraph:

    # 构造函数，从文件或命令行读取边
    def __init__(self):
        self._e = 0
        self._adj = dict()
        self.lpath = []

    #
    def add_edge(self, v, w, weight):
        if not self.hasVertex(v): self._adj[v] = {}
        if not self.hasVertex(w): self._adj[w] = {}
        if not self.hasEdge(v, w):
            self._e += 1
            self._adj[v][w] = int(weight)
            self._adj[w][v] = int(weight)

    #
    def adjacentTo(self, v):
        return iter(self._adj[v])

    #
    def vertices(self):
        return iter(self._adj)

    #
    def hasVertex(self, v):
        return v in self._adj

    #
    def hasEdge(self, v, w):
        return w in self._adj[v]

    #
    def countV(self):
        return len(self._adj)

    #
    def countE(self):
        return self._e

    #
    def degree(self, v):
        return len(self._adj[v])

    def print_path(self, l, o):
        for x in l:
            # print("%s -> "%x, end='')
            o.write("%s -> " % x)
        # print("\n", end='')
        o.writeln()

    def allpath(self, s, t, o):
        self.lpath += [s]
        if (s == t):
            self.print_path(self.lpath, o)
        else:
            for v in self.adjacentTo(str(s)):
                if (v not in self.lpath):
                    self.allpath(v, t, o)
        self.lpath.pop()

    def __findShorestNode(self, cost, visited):
        minDist = MAXL
        node = None
        for i in self.vertices():
            if (cost[i] < minDist) and (i not in visited):
                minDist = cost[i]
                node = i
        return node

    # 返回从源结点s到所有每个结点的最短路径代价字典cost，和路径指向字典 parents
    # cost[i]就是从s到达i的最小代价值，parents[i]存储从s到达i的最短路径上, i的前一个结点
    def dijkstra(self, s):
        cost = {}
        visited = [s]
        parents = {s: None}
        # 初始化cost字典
        for v in self.vertices():
            if self.hasEdge(s, v):
                cost[v] = self._adj[s][v]
            else:
                cost[v] = MAXL
        cost[s] = 0
        # 初始化parents字典
        for i in self.adjacentTo(s):
            parents[i] = s

        node = self.__findShorestNode(cost, visited)
        while node:
            for i in self.adjacentTo(node):  # 所有node结点的邻居结点
                newcost = cost[node] + self._adj[node][i]
                if newcost < cost[i]:
                    parents[i] = node  # 最短路径到达i的路径上，i的上一个结点是node
                    cost[i] = newcost
            visited.append(node)
            node = self.__findShorestNode(cost, visited)

        return cost, parents

    #
    def __str__(self):
        s = ''
        for v in self.vertices():
            s += v + '  '
            for w in self.adjacentTo(v):
                s += w + ' '
            s += '\n'
