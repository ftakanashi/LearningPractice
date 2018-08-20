# -*- coding:utf-8 -*-

'''
Dijkstra中文译名迪科斯彻，是荷兰的计算机学家。
Dijkstra算法主要用于寻找图中从某一点到各个点的最短路径。自然，这个算法的输入是一个图和图中的一个点，输出则是每个点到指定点的最短路径
从算法的结构上来看，Dijkstra算法和Prim算法如出一辙，Prim算法以每条边的权值作为优先度求mst
，而Dijkstra算法以某一条边到达其终点后终点的累计路径作为优先度，可以联合记忆

关键词：优先队列，定长初始化结果集，算法结构和Prim算法的类似性
'''

import Queue

def dijkstra(graph,v):
    vnum = graph.vertex_num()
    minp = [None] * vnum
    queue = Queue.PriorityQueue()
    queue.put((0,v,v))    # 已起始点到起始点的路径为0，作为自洽条件率先入队
    count = 0    # 提前跳出的辅助变量
    while count < vnum and not queue.empty():
        p,vi,vj = queue.get()
        if minp[vj] is not None:
            continue
        minp[vj] = (p,vi)
        count += 1
        for edge in graph.out_edges(vj):
            for fp,fvj in edge:
                if minp[fvj] is not None:
                    continue
                queue.put((fp+p,vj,fvj))

    return minp