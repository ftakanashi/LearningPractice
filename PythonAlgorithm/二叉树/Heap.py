# -*- coding:utf-8 -*-

import sys

# -*- coding:utf-8 -*-
import sys

class Heap:
    '''
    基本堆类
    '''
    def __init__(self,lst):
        self._elems = list(lst)
        self.buildHeap()

    def __len__(self):
        return len(self._elems)

    def shiftDown(self,ele,start,end):
        i,c1,c2 = start,start*2+1,start*2+2
        while c2 <= end or c1 <= end:
            if c2 <= end and self._elems[c2] < self._elems[c1]:
                j = c2
            else:
                j = c1
            if ele > self._elems[j]:
                self._elems[i] = self._elems[j]
                i,c1,c2 = j,j*2+1,j*2+2
            else:
                break
        self._elems[i] = ele

    def shiftUp(self,ele,start,end):
        i,p = end,(end-1)//2
        while p > start and ele < self._elems[p]:
            self._elems[i] = self._elems[p]
            i = p
            p = (i-1)//2
        self._elems[i] = ele

    def buildHeap(self):
        end = len(self._elems) - 1
        for i in range((end-1)//2,-1,-1):
            self.shiftDown(self._elems[i],i,end)

    def top(self):
        return self._elems[0]

    def showElem(self):
        print self._elems

    def showTree(self):
        '''
        将一个列表以常见的树形结构打印出来。存在一定误差，十分简易
        :return:
        '''
        totalLen = len(self._elems)
        layerCount = 0
        flag = 0
        while totalLen > flag:
            flag += pow(2,layerCount)
            layerCount += 1

        totalWidth = pow(2,layerCount-1) * 3 - 2
        def showLine(slice,layer):
            slice = list(slice)
            length  = pow(2,layer)
            if len(slice) < length:
                slice.extend(list(' ' * (length-len(slice))))  # 用空格补齐本行到2的次方个数，防止最后一行输出错乱
            wsLen = (totalWidth - length) / (length + 1)
            for item in slice:
                sys.stdout.write(' '*wsLen)
                sys.stdout.write(str(item))
            sys.stdout.write(' '*wsLen)
            sys.stdout.write('\n')

        # for layer in range(layerCount):
        #     print self._elems[pow(2,layer)-1:pow(2,layer+1)-1]
        for layer in range(layerCount):
            showLine(self._elems[pow(2,layer)-1:pow(2,layer+1)-1],layer)


class HeapQueue(Heap):
    '''
    基于堆构建优先队列
    '''
    def dequeue(self):
        tmp = self._elems[0]
        target = self._elems.pop()
        if len(self._elems) > 0:
            self.shiftDown(target,0,len(self._elems)-1)
        return tmp

    def enqueue(self,newEle):
        self._elems.append(newEle)
        self.shiftUp(newEle,0,len(self._elems)-1)

class HeapSorter(HeapQueue):
    '''
    可用于排序的堆类
    '''
    def sort(self):
        for i in range(len(self._elems)-1,-1,-1):
            tmp = self.top()
            self.shiftDown(self._elems[i],0,i)
            self._elems[i] = tmp

def heap_sort(lst):
    '''
    独立的堆排序函数
    :param lst:
    :return:
    '''
    elems = lst
    def shift_down(elems,ele,start,end):
        i,c1,c2 = start,start*2+1,start*2+2
        while c2 <= end or c1 <= end:
            if c2 <= end and elems[c2] < elems[c1]:
                j = c2
            else:
                j = c1
            if ele > elems[j]:
                elems[i] = elems[j]
                i,c1,c2 = j,j*2+1,j*2+2
            else:
                break
        elems[i] = ele
    for i in range((len(elems)-2)//2,-1,-1):  # 构造堆
        shift_down(elems,elems[i],i,len(elems)-1)
    for end in range(len(elems)-1,-1,-1):  # 进行排序
        target = elems[0]
        shift_down(elems,elems[end],0,end-1)
        elems[end] = target

if __name__ == '__main__':
    import random
    ls = range(27)
    random.shuffle(ls)
    # heap_sort(ls)
    heap = Heap(ls)
    heap.showTree()
    heap.showElem()