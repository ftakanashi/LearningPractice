# -*- coding:utf-8 -*-

def knapsack(weights,values,pack):
    num = len(weights)
    # vtable = [0] * (pack+1)
    vtable = [0] + ([float('-inf')] * pack)
    for i in range(num):
        weight = weights[i]
        value = values[i]
        for j in range(pack,weight-1,-1):
            # if j - weight < 0:
            #     continue
            vtable[j] =  max(vtable[j],vtable[j-weight]+value)

    return vtable

# print knapsack([2,2,6,5,4],[6,3,5,4,6],10)
# [2,2,4,5,6]
# [1,3,6,4,5]
def preprocess(_weights,_values,pack):
    def double_sort(w,v,left,right):
        if left >= right:
            return
        pivot = w[left]
        i = idx = left + 1
        while i <= right:
            if w[i] <= pivot:
                w[idx],w[i] = w[i],w[idx]
                v[idx],v[i] = v[i],v[idx]
                idx += 1
            i += 1
        idx = idx - 1
        w[left],w[idx] = w[idx],w[left]
        v[left],v[idx] = v[idx],v[left]
        double_sort(w,v,left,idx-1)
        double_sort(w,v,idx+1,right)

    weights,values = list(_weights),list(_values)
    leng = len(weights)
    double_sort(weights,values,0,leng-1)
    print weights
    print values
    max,maxIdx,drop = values[0],0,[]
    for i in range(1,leng):
        if weights[i] > pack:
            drop.append(i)
            continue
        if max >= values[i]:
            drop.append(i)
        else:
            if weights[maxIdx] == weights[i]:
                drop.append(maxIdx)
            max = values[i]
            maxIdx = i

    resWeight = [weights[i] for i in range(leng) if i not in drop]
    resValue = [values[i] for i in range(leng) if i not in drop]

    return resWeight,resValue

def totalknap(weights, values, pack):
    num = len(weights)
    # vtable = [0] * (pack + 1)
    vtable = [0] + [float('-inf')] * pack
    for i in range(num):
        weight = weights[i]
        value = values[i]
        for j in range(weight,pack+1):
            vtable[j] = max(vtable[j], vtable[j-weight] + value)

    return vtable

import random
print totalknap([2,2,6,5,4],
                 [0,1,5,4,6],10)
