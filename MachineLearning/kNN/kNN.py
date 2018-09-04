# -*- coding:utf-8 -*-

'''
kNN主要用于分类。处理对象通常是可以转化成一个向量的东西。基本思想：
1. 计算已知类别数据集中所有点和当前所求点的距离。排序距离
2. 找出距离最小的前k个点
3. 确定k个点的类别的出现频率
4. 返回出现频率最高者作为当前点的类别预测

'''
from numpy import *
from collections import Counter
'''
用到的公式:
两点间的距离，不论是二维三维还是N维，都是各维度差的平方的和，再开平方根。（用numpy.array的批量计算特性很方便）
考虑到各个维度间绝对值可能差很多，还需要归一化
'''

def classify0(inX,dataSet,labels,k):
    '''
    核心函数，理想情况下用来返回某个待分类向量的类别
    :param inX:  待分类向量
    :param dataSet:  已分类向量集
    :param labels:  已分类向量集的标签集
    :param k:  自定义选取距离最近的k个点，可作为一个超变量
    :return:
    '''
    dataSetSize = dataSet.shape[0]    # shape[0]是已分类向量集的第一维长度（行数），即有多少条已分类向量
    batchInx = tile(inX,(dataSetSize,1))  # 构造一个行数规模和已分类数据集相同的“批量”待分类向量
    diffMatrix = batchInx - dataSet
    squareMatrix = diffMatrix ** 2
    squareDistSum = squareMatrix.sum(axis=1)
    distances = squareDistSum ** 0.5    # distance是个shape是(1,N)的向量，表示inX与dataSet中每个点之间的距离
    distSortedIndex = distances.argsort()

    count = Counter()
    for i in range(k):
        label = labels[distSortedIndex[i]]
        count.update(label)
    return count.most_common(1)[0][0]    # 利用了collections.Counter，做了简单的计数，找出计数最多的分类

def autoNorm(dataSet):
    '''
    归一化函数，采用线性归一的办法，将各个维度绝对量差距较大时尽量统一化，使每个维度对分类影响都差不多
    线性归一化公式：(value - minValue) / (maxValue - minValue)，归一化后值的范围是(0,1)，
    :param dataSet:
    :return:
    '''
    dataSetSize = dataSet.shape[0]
    minValue = dataSet.min(0)    # 每个维度的最小值组成的向量
    maxValue = dataSet.max(0)    # 每个维度的最大值组成的向量
    valRange = maxValue - minValue
    newDataSet = (dataSet - tile(minValue,(dataSetSize,1))) / (tile(valRange,(dataSetSize,1)))
    return newDataSet

print autoNorm(array([[0.25,11000,12.8],[0.3,12100,10.0],[0.11,14000,8],[0.21,15300,11]]))


