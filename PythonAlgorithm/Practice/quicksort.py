# -*- coding:utf-8 -*-

def quick_sort(lst,left,right):
    if right <= left:
        return
    pivot = lst[left]
    i = left + 1
    idx = i
    while i <= right:
        if lst[i] < pivot:
            lst[i],lst[idx] = lst[idx],lst[i]
            idx += 1
        i += 1
    idx = idx - 1
    lst[left],lst[idx] = lst[idx],lst[left]
    quick_sort(lst,left,idx-1)
    quick_sort(lst,idx+1,right)

import random
lst = range(100)
random.shuffle(lst)
quick_sort(lst,0,len(lst)-1)
print lst
