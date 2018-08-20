# -*- coding:utf-8 -*-

class Assoc:
    def __init__(self,key,value):
        self.key = key
        self.value = value

    def __lt__(self, other):
        return self.key < other.key

    def __le__(self, other):
        return self.key <= other.key

    def __str__(self):
        return 'Assoc({0},{1})'.format(self.key,self.value)

class DictList:
    def __init__(self):
        self._elems = []

    def is_empty(self):
        return not self._elems

class OrderedDictList(DictList):

    def search(self,key):
        low,high = 0,len(self._elems)
        while low <= high:
            mid = low + (low + high) // 2
            if key == self._elems[mid].key:
                return self._elems[mid]
            if key < self._elems[mid].key:
                high = mid - 1
            else:
                low = mid + 1

    def insert(self,key,data):
        i = 0
        while i < len(self._elems):
            if self._elems[i].key > key:
                break
            i += 1
        self._elems.insert(i,data)

    def delete(self,key):
        i = 0
        tgt = None
        while i < len(self._elems):
            if self._elems[i].key == key:
                tgt = self._elems.pop(i)
            i += 1
        return tgt


def str_hash(string,res):
    h1 = 0
    for c in string:
        h1 = h1 * 29 + ord(c)
    tgtidx = h1 % 31
    def h2(h1):
        return h1 % 5 + 1
    count = 0
    while res[tgtidx] is not None:
        tgtidx = (tgtidx + h2(h1)) % 31
        count += 1
        if count > 31:
            break
    res[tgtidx] = string

rr = [None] * 8
str_hash('FrankNihao01+==',rr)
for i in 'abcdef':
    str_hash(i,rr)
print rr
