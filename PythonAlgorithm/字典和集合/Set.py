# -*- coding:utf-8 -*-

'''
顺序表实现相比于普通连续表实现好处多多。
比如查找的时候可以使用二分法查找从而把查找效率从O(n)提升到O(logn)
再比如，顺序表实现的集合求交集的时候，可以通过O(m+n)的复杂度而不是O(m*n)来求解。比如下面这个方法
'''

def intersect(setA,setB):
    '''
    修改部分代码也可以做成求并集或者差集的函数
    保持O(m+n)的复杂度的同时
    :param setA:
    :param setB:
    :return:
    '''
    i,j = 0,0
    res = []
    while i < len(setA) and j < len(setB):
        if setA[i] == setB[j]:
            res.append(setA[i])
            i += 1
            j += 1
        elif setA[i] < setB[j]:
            i += 1
        else:
            j += 1

    return res

'''
由于集合中元素不可重复出现，即不能有冲突。所以可以考虑用散列表的技术来实现集合。联系字典，其实字典中各个key形成的就是一个集合。
如果采用散列表实现，那么具体的散列方法、冲突消解策略都会影响到集合结构的操作效率
'''
import random
class HashSet:
    '''
    未完成
    '''
    def __init__(self,length):
        self._elems = [None] * length
        self._root = length
        self._root2 = random.choice([5,7,11,13])

    def _locate(self,_elem):
        if not isinstance(_elem,int):
            elem = self._numize(_elem)
        else:
            elem = _elem
        i = elem % self._root
        try_count = 0
        while self._elems[i] is not None:
            i = (i + i * ( elem % self._root2 + 1 )) % self._root
            try_count += 1
            if try_count > self._root:
                break
        self._elems[i] = _elem

    def _numize(self,s):
        res = 0
        for c in s:
            res = res * 31 + ord(c)
        return res

    def add(self,elem):
        self._locate(elem)

    def show(self):
        print self._elems


'''
集合还有一种特殊的表现形式，称为位向量。其实就是将所有要表示的集合的超集看作是每个位都是1的N维向量。
然后针对每个集合（也是超集U的子集）表现为若干特定位为0的N维向量，表示这些位置的元素不存在于本集合中
如令{a,b,c,d,e} = 11111
那么集合{a,c,d} = 10110
'''
