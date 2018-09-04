#-*- coding:utf-8 -*-

class TreeNode:
    def __init__(self,value,root,left,right):
        self.value = value
        self.root = root
        self.left = left
        self.right = right

class Heap:
    def __init__(self,elems):
        self.elems = list(elems)
        self.leng = len(self.elems) - 1
        for j in range((self.leng-1) // 2,-1,-1):
            self.heapify(j)

    def heapify(self,i,leng=-1):
        if leng == -1:
            leng = self.leng
        tmp = self.elems[i]
        l,r = i * 2 + 1, i * 2 + 2
        while l <= leng or r <= leng:
            if r < leng and self.elems[r] < self.elems[l]:
                tgt = r
            else:
                tgt = l
            if tmp > self.elems[tgt]:
                self.elems[i] = self.elems[tgt]
                i,l,r = tgt, tgt * 2 + 1, tgt * 2 + 2
            else:
                break
        self.elems[i] = tmp

    def sort(self):
        for i in range(self.leng,0,-1):
            self.elems[0],self.elems[i] = self.elems[i],self.elems[0]
            self.heapify(0,i-1)


import random
lst = range(100)
random.shuffle(lst)
print lst
heap = Heap(lst)
print heap.elems
heap.sort()
print heap.elems
