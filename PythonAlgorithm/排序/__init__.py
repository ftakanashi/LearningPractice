# -*- coding:utf-8 -*-

'''
排序不仅仅是解决需要排序这一类问题，其他很多算法也要依靠排序完毕的结构来保证算法的正确运行
下面是几种常见排序算法。统一都是将序列按照关键码从小到大排序
序列中每个元素都是下面这种Record类对象
'''
class Record:
    def __init__(self,key,value):
        self.key = key
        self.value = value