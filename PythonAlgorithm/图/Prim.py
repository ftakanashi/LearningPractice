# -*- coding:utf-8 -*-
'''
Prim算法和Kruskal类似，用来获得图的一棵最小生成树
输入是一个图（以GraphAL实现为例），输出是一个列表形式记录的最小生成树，记录树中每条边的 两个端点和权值
算法中用到的额外结构包括一个以边的权值作为优先度的有限队列
关键词：优先队列保证权值最小, 定长mst列表初始化方便进行已确定的判断

算法复杂度：
时间复杂度 O(ElogE)，因为每条边至少入队一次，所以主循环的复杂度是这样
空间复杂度 O(E)，mst和queue的使用分别是O(V)和O(E)的。但是在连通图中V<=E,所以取E。
'''

import Queue

queue = Queue.PriorityQueue()

def prim(graph):
    vnum = graph.vertex_num()
    mst = [None] * vnum    # 采用定长初始化数组，这样可以不用额外再维护一个结构，或者每次都循环扫描mst来判断某个点是否已经存在于mst中
    count = 0   # 由于mst是定长声明的，无法再使用len(mst)来判断生成树是否已经完整，所以额外搞一个count来记录mst中不是None的记录。不使用None in mst来判断是因为这是O(V)的操作
    queue.put((0,0,0))    # 为了保证程序的自洽性，需要加入一个初始元素到队列中。可以理解为，初始点到其本身有一条权值为0的边
    while count < vnum and not queue.empty():
        w,vi,vj = queue.get()
        if mst[vj] is not None:    # 如取出一条边的终点端点已经有记录，说明之前通过一条更短的路径已经到达了它，因此这次遍历到的这条边可以直接跳过
            continue
        mst[vj] = (w,vi,vj)
        count += 1    # 又加入了一条新边到mst中
        for v,w in graph.out_edges(vj):
            if mst[v]:
                continue
            queue.put((w,vj,v))    # 计算复杂度的时候不要忽视了对于优先队列入队通常还要O(logn)的时间

    return mst



