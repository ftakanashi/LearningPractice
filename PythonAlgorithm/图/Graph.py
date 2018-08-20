# -*- coding:utf-8 -*-

import copy

class GraphException(Exception):
    pass

class Graph:
    '''
    基于邻接矩阵的图类
    '''
    def __init__(self,mat,unconn=0):
        vnum = len(mat)
        for x in mat:
            if len(x) != vnum:
                raise GraphException('Invalid row of graph')
        self._mat = copy.deepcopy(mat)  # 记得拷贝哦
        self._unconn = unconn
        self._vnum = vnum

    def vertex_num(self):
        '''
        返回方阵的长or宽
        :return:
        '''
        return self._vnum

    def _invalid(self,*args):
        '''
        检查某个下标是否合法。由于在其他方法中会经常用到所以特别定义了个单独的
        :param v:
        :return:
        '''
        for v in args:
            if v < 0 or v > self._vnum:
                return True

        return False

    def add_vertex(self,val):
        '''
        增加一个新节点的方法，暂时先不实现
        :param val:
        :return:
        '''
        pass

    def add_edge(self,v1,v2,val):
        '''
        新增或者是去更新一条边的权值
        :param v1:
        :param v2:
        :param val:
        :return:
        '''
        if self._invalid(v1,v2):
            raise GraphException('Invalid index')
        self._mat[v1][v2] = val

    def get_edge(self,v1,v2):
        if self._invalid(v1,v2):
            raise GraphException('Invalid index')
        return self._mat[v1][v2]


    @staticmethod
    def _out_edges(row,unconn):
        for i in range(len(row)):
            yield i,row[i]

    def out_edges(self,v1):
        if self._invalid(v1):
            raise GraphException('Invalid index')
        return self._out_edges(self._mat[v1],self._unconn)

class GraphAL(Graph):
    '''
    基于邻接表的图实现
    '''
    def __init__(self,mat,unconn=0):
        vnum = len(mat)
        for x in mat:  # 从一个规则方阵开始创建邻接表
            if len(x) != vnum:
                raise GraphException('Invalid mat')
        self._vnum = vnum
        self._unconn = unconn
        self._mat = []
        for i in range(vnum):  # 创立了一个邻接矩阵，虽然还是二维数组，但是每行长度不规则了
            row = []
            for j,val in sorted(enumerate(mat[i]),key=lambda x:x[1]):  # 保持邻接表内元素有序，这是有好处的
                if val == unconn or i == j: continue
                row.append((j,val))
            self._mat.append(row)
        # 需注意邻接表中每个元素是一个tuple，内容是(i,val)，i是目标节点下标，val是本边权值

    def getMat(self):
        return self._mat

    def add_vertex(self,val):
        '''
        为图新增一个节点
        :param val:
        :return:
        '''
        self._mat.append([])    # 默认新加入节点的出度表是空
        self._vnum += 1
        return self._vnum - 1 # 返回新加入的节点的下标

    def add_edge(self,v1,v2,val):
        if self._invalid(v1,v2):  # vnum是0，即空图的情况也算在里面了
            raise GraphException('Invalid index')
        row = self._mat[v1]
        i = 0
        while i < len(row):
            tgt,vav = row[i]
            if tgt == v2:
                row[i][1] = val
                return
            if v2 > tgt:
                break
            i += 1
        row.insert(i,(v2,val))

    def get_edge(self,v1,v2):
        if self._invalid(v1,v2):
            raise GraphException('Invalid index')
        for i,val in self._mat[v1]:
            if i == v2:
                return val
        return self._unconn

    def out_edges(self,v1):
        if self._invalid(v1):
            raise GraphException('Invalid Indedx')
        return self._mat[v1]

    def DFStraversal(self,start,proc):
        '''
        基于邻接表的深度优先遍历节点
        :param start:
        :return:
        '''
        import Queue
        visited = [0] * self.vertex_num()    # 构造一个已访问数组记录已访问的节点，避免环路
        visited[start] = 1
        if len(self._mat[start]) == 0:  # 若遍历开始的节点就是独立的，那么直接处理后返回
            proc(start)
            return
        stack = Queue.LifoQueue()
        stack.put((0,self._mat[start]))    # 栈中保存的数据格式(计划访问出度表中的下标，出度表)，而出度表每个元素的格式是(目标节点的下标，边的权值)
        while not stack.empty():
            i,nodes = stack.get()
            if i < len(nodes):  # 计划访问的节点确实存在于出度表中
                tgt,val = nodes[i]
                stack.put((i+1,nodes))  # 将出度表中下一个节点加入栈，计划下次回到本节点时访问的就是出度表中下标为i+1的节点
                if not visited[tgt]:    # 若访问表中记录该节点已经访问过了，就不要再访问了。
                    proc(tgt)
                    visited[tgt] = 1
                    stack.put((0,self._mat[tgt]))  # 如果tgt节点还有后续节点，那么优先将这些节点入栈，进行深度优先的处理。
                    # 这里没有做下标为tgt的节点是否有后续节点的判断，因为这个循环完了后马上又从栈中取出来，在上面i<len(nodes)会有判断的
