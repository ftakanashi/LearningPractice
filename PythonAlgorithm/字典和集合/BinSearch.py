# -*- coding:utf-8 -*-

def bin_search(lst,key):
    low,high = 0,len(lst)-1
    while low <= high:
        mid = low + ( high - low ) // 2
        if key == lst[mid].key:
            return lst[mid]
        if key < lst[mid].key:
            high = mid - 1
        else:
            low = mid + 1
