# -*- coding:utf-8 -*-

def bin_search(lst,key):
    low,high = 0,len(lst)-1
    while low <= high:
        mid = low + ( high - low ) // 2  # 这里没有单纯的 (low + high) // 2
        if key == lst[mid].key:
            return lst[mid]
        if key < lst[mid].key:
            high = mid - 1
        else:
            low = mid + 1

def binsearch(lst,target):
    low,high = 0,len(lst)-1
    while low <= high:
        mid = (low + high) // 2
        if lst[mid] == target:  return mid
        if lst[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

if __name__ == '__main__':
    print binsearch([1,2,4,5,8,10,15],2)
