# -*- coding:utf-8 -*-

'''
AOV网指节点活动网。是一个有向图。通常实际意义是用来表示各个节点之间的先后关系。若a节点指向b，则表示必须完成a节点才能进行b节点。
这类网可能可以导出一个拓扑序列，使得所有有(vi,vj)边时，vj节点排在vi节点后面。可以导出的充要条件是图中没有回路
朴素的求拓扑序列算法很简单：
  持续找图中入度为0的点，拿出来加入拓扑序列，然后将节点删除。删除时自然其出度指向的所有节点的入度都减一
但是这个算法每次都要扫描全图，不太好。借鉴八皇后问题用数组的下标本身作为信息的一个维度的想法
我们可以建立一个统计各个节点入度的列表。当入度减为0的时候将对应下标的节点入拓扑序列，然后其出度节点对应的入度表元素减一。
这样直到拓扑序列长度为图节点个数或者表中没有入度为0的节点。（后者其实表示图中其实有回路，即无拓扑序列。

实现的时候还可以继续优化。因为寻找入度为0的元素还是要扫描整个入度表，一旦某个节点入度归零且入了拓扑序列，那么入度表中这个位置其实已经没用了
此时可以将这些位置充分利用起来。做法就是充分利用入度表空间，手动创建维护一个入度表内部的栈，具体实现看下面代码

关键词：入度表；入度表内的模拟栈；通过正确时应该要遍历vnum次作为前提，来进行循环限制和回路时返回错误

时间复杂度是O(E+V)，而空间复杂度就是O(V)
'''

def topology_sort(graph):
    vnum = graph.vertex_num()
    indegree,toposeq = [0] * vnum,[]
    last_vzero_idx = -1

    for vi in range(vnum):    # 初始化入度表
        for v,w in graph.out_edges(vi):
            indegree[v] += 1

    for v in range(len(indegree)):    # 初始化入度表中的“栈”，其结构类似于[..., -1(下标为j), ..., j(下标为k), ...]，另外再加上独立的一个变量last_vzero_idx作为栈顶，值为k
        if indegree[v] == 0:
            indegree[v] = last_vzero_idx
            last_vzero_idx = v

    for _ in range(vnum):    # 理想情况是处理vnum次，所以是range(vnum)
        if last_vzero_idx == -1:    # 还未处理够vnum次，就发生了0入度的节点遍历完了的情况，说明图中存在回路，因此无解
            return False
        vi = last_vzero_idx
        last_vzero_idx = indegree[last_vzero_idx]
        toposeq.append(vi)
        for v,w in graph.out_edges(vi):    # 从本节点出发的出度终点节点，入度都要减一
            indegree[v] -= 1
            if indegree[v] == 0:    # 一旦发现入度减为0了，那么可以将本节点“入栈”，即入度表中的本节点下标位置存储上一个入度为0的节点的下标，而本节点下标存入last_vzero_idx
                indegree[v] = last_vzero_idx
                last_vzero_idx = v

    return toposeq