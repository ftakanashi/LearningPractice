# -*- coding:utf-8 -*-

def merge(l1,l2):
    i,j = 0,0
    res = []
    while i < len(l1) and j < len(l2):
        if l1[i] <= l2[j]:
            res.append(l1[i])
            i += 1
        else:
            res.append(l2[j])
            j += 1
    while i < len(l1):
        res.append(l1[i])
        i += 1
    while j < len(l2):
        res.append(l2[j])
        j += 1

    return res

def merge_sort(lst,left,right):
    if left >= right:
        return [lst[left]]
    mid = (left + right) // 2
    return merge(merge_sort(lst,left,mid),merge_sort(lst,mid+1,right))

if __name__ == '__main__':
    import random
    lst = range(10)
    random.shuffle(lst)
    print merge_sort(lst,0,len(lst)-1)