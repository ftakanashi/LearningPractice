# -*- coding:utf-8 -*-
from numpy import *
from collections import Counter

import os
import random
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def line2vec(line):
    s = line.split()
    label = s[-10:]
    tmp = []
    for digit in s[:-10]:
        tmp.append(int(float(digit)))
    return tmp,label

def loadData(testSize=100):
    with open(os.path.join(BASE_DIR,'semeion.data'),'r') as f:
        lines = f.readlines()
    total = len(lines)
    testSet = zeros((testSize,256))
    testLabels = zeros((testSize,10))
    trainSet = zeros((total-testSize,256))
    trainLabels = zeros((total-testSize,10))

    for i in range(testSize):
        randIdx = random.randint(0,total-1)
        total -= 1
        line = lines[randIdx]
        del(lines[randIdx])
        vec,label = line2vec(line)
        testSet[i] = vec
        testLabels[i] = label

    for i,line in enumerate(lines):
        vec,label = line2vec(line)
        trainSet[i] = vec
        trainLabels[i] = label
    return trainSet,trainLabels,testSet,testLabels

def classify(entry, dataSet,labels, k):
    dataSetSize = dataSet.shape[0]
    batchEntry = tile(entry,(dataSetSize,1))
    distances = (((batchEntry - dataSet) ** 2).sum(axis=1)) ** 0.5
    sortDistIndex = distances.argsort()
    c = Counter()
    for i in range(k):
        c.update(str(onehot(labels[sortDistIndex[i]])))
    return c.most_common(1)[0][0]

def onehot(label):
    for i,flag in enumerate(label):
        if flag == 1:
            return i

def main():
    trainSet, trainLabels, testSet, testLabels = loadData(testSize=50)
    k = 3
    rightCount = 0
    for i,row in enumerate(testSet):
        probLabel = classify(row,trainSet,trainLabels,k)
        realLabel = str(onehot(testLabels[i]))
        print 'Guess digit is %s, and right answer is %s' % (probLabel,realLabel)
        if probLabel == realLabel:
            rightCount += 1

    print 'success count %s' % rightCount

if __name__ == '__main__':
    main()