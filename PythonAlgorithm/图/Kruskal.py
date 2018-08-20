# -*- coding:utf-8 -*-
'''
Kruskal算法用来获得图的一棵最小生成树
输入是一个图（以GraphAL实现为例），输出是一个列表形式记录的最小生成树，记录树中每条边的 两个端点和权值
算法中途要用的辅助结构包括一个reps列表用来记录每个端点所在联通分量的代表元
关键词：有序的边列表，代表元，直到只剩一个联通分量为止

算法复杂度：
时间复杂度 O(max(ElogE,V^2))
空间复杂度 O(E)
'''
def kruskal_mine(graph):
    vnum = graph.vertex_num()
    edges = []
    for vi,out_edges in enumerate(graph.getMat()):
        for vj,weight in out_edges:
            edges.append((weight,vi,vj))
    edges.sort(key=lambda x:x[0])

    reps = range(vnum)
    mst = [None] * vnum
    for edge in edges:
        w,vi,vj = edge
        if reps[vi] == reps[vj]:
            continue
        mst[vj] = (w,vi)
        for i in range(len(reps)):
            if reps[i] == reps[vj]:
                reps[i] = reps[vi]
        reps[vj] = reps[vi]
    return mst

def kruskal(graph):
    vnum = graph.vertex_num()
    reps = [i for i in range(vnum)]  # 最开始没有连接任何一条边，所以所以联通分量的代表元都是端点自己
    mst,edges = [],[]    # 不用[None] * vnum来初始化mst，方便在主循环里面做一个小优化
    for vi in range(vnum):  # 把所有边都整合在一起然后按照权值排序
        for v,w in graph.out_edges(vi):
            edges.append((w,v,vi))
    edges.sort()
    for w,vi,vj in edges:  # 从权值最小者开始遍历各个边，有需要就将这个边连起来（就是将边的信息加入了mst中）
        if reps[vi] == reps[vj]:    # vi和vj已经处于同一联通分量，可以直接跳过
            continue
        mst.append((w,vi,vj))
        if len(mst) >= vnum - 1:  # 小优化,达到vnum-1说明已经有了完整的生成树，可以结束遍历
            break
        for i,repv in enumerate(reps):
            if reps[i] == reps[vj]:
                reps[i] = reps[vi]
        reps[vj] = reps[vi]
    return mst