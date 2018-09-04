# -*- coding:utf-8 -*-

'''
用于分类，可将模型持久化
基本思想：
1. 找出一个对当前数据集而言最具特征的属性（找这个属性通常是尝试每一种属性，看哪种属性分类后的子集香浓熵最低
2. 将这种特征抽取出来，并以此判断为基础构建树的一个节点。对于未能通过这个特征取得较好分类的子集进行递归地合适特征搜索
3. 直到所有特征都被抽取完或当前数据集已经纯净，构建叶节点，并为叶节点打上当前数据集中多数的label作为这个叶节点的分类结果标记。
这种决策树算法会“消耗”特征，也有一些其他实现可以避免特征的不断被消耗
'''

import math
import collections
from numpy import array
'''
香农熵：
数据集D的香农熵计算公式 Ent(D) = -sum( pk * log2(pk) )  其中k是数据集D中数据的种类数，
比如当k=1，即数据集中只有一种类型的数据的时候，log2(pk) = 0。说明此时熵最小，为0。
'''
def getShannonEnt(labels):
    '''
    计算香农熵的函数。传入一个标签集，返回一个香农熵结果
    '''
    counts = collections.defaultdict(int)
    for label in labels:
        counts[label] += 1
    ent = 0.0
    total = len(labels)
    for label,count in counts.iteritems():
        prob = float(count)/total
        ent += prob * math.log(prob,2)
    return -ent
'''
信息增益：
香农熵只是做出了对一个数据集混乱程度的评价，而作为我们要找出一个合理的划分数据集的指标，就要另寻他路。
信息增益可以用来衡量指标的合理性，选定一个指标后，首先要找到指标可能的取值
然后计算每个指标的每个取值划分出来的子数据集的熵，做一些修正（绝对量修正）后把这些熵加在一起，得到的总熵和原熵作比较，所得的差就是信息增益
具体的计算公式
Gain(D,a) = Ent(D) - sum( ((len(Dv) / len(D)) * Ent(Dv) )。其中v的取值是指标a可能的取值种数，而Dv代表a取到特定的值av时那些记录组成的D的子集。
总体而言，某个分类指标a，各个取值分出来的子集子集越大且越纯净，体现出来公式后半部的sum就越小，从而Gain就越大。
信息增益Gain(D,a)越大，表示a越适合做 构建决策树时划分D数据集的依据
'''
def getGainForAttr(dataSet,attrIdx,labels,totalEnt):
    '''
    计算单个属性的信息增益情况
    :param dataSet: 数据集
    :param attrIdx: 属性位于向量中的下标位置
    :param labels: 标签集
    :param totalEnt: 原标签集的香农熵
    :return:
    '''
    attrs = set([])
    subLabels = collections.defaultdict(list)
    for i,row in enumerate(dataSet):
        attr = row[attrIdx]
        attrs.add(attr)  # attrs收集该属性所有可能的取值
        subLabels[attr].append(labels[i])  # subLabels收集属性取某个具体值时被划分出来的子数据集的标签情况

    attrEnt = 0.0
    totalCount = float(len(labels))
    for attr in attrs:
        attrEnt += len(subLabels[attr])/totalCount * getShannonEnt(subLabels[attr])  # 计算每个子数据集的熵并相加

    return totalEnt - attrEnt


def getClassifyAttr(dataSet,labels):
    '''
    寻找最佳分类属性
    '''
    dataSetSize,totalAttribute = dataSet.shape
    totalEnt = getShannonEnt(labels)
    maxGain = float('-inf')
    maxGainAttrIdx = None
    for i in range(totalAttribute):  # 遍历每个属性
        attrGain = getGainForAttr(dataSet,i,labels,totalEnt)  # 计算每个属性的信息增益
        if attrGain > maxGain:  # 保存信息增益的最大者
            maxGainAttrIdx = i
            maxGain = attrGain
    return maxGainAttrIdx
'''
以一个实例来说明香农熵 和 信息增益
比如按西瓜书，看某个瓜是否是好瓜，给出了以下数据集，各个字段分别是色泽，敲声，是否是好瓜判断
青色  清脆  好瓜
乌黑  浊响  好瓜
浅白  清脆  坏瓜
青色  沉闷  坏瓜
就这个数据集D而言，Ent(D)等于 -sum( pk * log2(pk)) 即 - 2*(0.5 * log2(0.5)) = 1  //顺便也可以看出香农熵可以大于1的
而如果按照色泽作为划分依据，那么Gain(D,a)等于Ent(D) - (0.5*1 + 0.25*0 + 0.25*0)  //色泽取值乌黑或者浅白的时候，记录都只有一条，因此熵是0。取色泽是青色的时候刚好熵也是1
'''
'''
增益率的概念：
使用信息增益有一个潜在的缺陷，当某个分类依据的取值有很多很多，多到每个记录这个分类依据的取值都不同
此时显然Gain(D,a)计算公式的后半部，求和公式中每一项都是 [1/len(D)]*0，此时增益很大。但是这种模型显然不具有泛化能力。
因此提出了用增益率代替信息增益绝对值作为标准。
Gain_Ratio(D,a) = Gain(D,a) / IV(a)。其中IV(a) = -sum( Lv * log2(Lv) )而Lv是len(Dv)/len(D)，v从1取到指标a可以取值的总数
可以看出，增益率公式中的IV(a)这一项，在确定a是哪个指标之后就定了，是指标a的固有属性。注意区分IV(a)和香农熵的区别。
前者是选定一个指标之后计算的熵，后者如果要和前者统一来看，那么可以认为选的指标是分类结果这一栏。
'''
def getGainRatioForAttr(dataSet,attrIdx,labels,totalEnt):
    '''
    计算单个属性的信息增益率，和计算信息增益绝对值的函数差不多
    '''
    attrs = set([])
    subLabels = collections.defaultdict(list)
    for i,row in enumerate(dataSet):
        attr = row[attrIdx]
        attrs.add(attr)
        subLabels[attr].append(labels[i])

    attrEnt = 0.0
    totalCount = float(len(labels))
    iv = 0.0
    for attr in attrs:
        attrRatio = len(subLabels[attr]) / totalCount    # 这个值要用两次了，所以单独列出来，其意义是某个属性值划分出子数据集占总数据集的比例
        attrEnt += attrRatio * getShannonEnt(subLabels[attr])
        iv += attrRatio * math.log(attrRatio,2)  # 主要区别在这里，加上了累加计算IV(a)的值的步骤。

    gain = totalEnt - attrEnt
    iv = -iv
    return gain / iv


'''
通过上述手段可以在一个特定数据集的情况下获取到划分这个数据集最优的属性。接下来就是实现如何来通过最优属性构造一棵树了。
关于实现树的数据结构，我们采用最简单的嵌套字典的形式。
对于通过一个最优属性划分出子数据集之后，这个子数据集作为叶子节点给出的判断可以简单地选择子数据集中众数label
另外别忘了得在可用的分类属性中将这次使用的属性删掉。
'''
def findPublicLabel(labels):
    '''
    寻找一个标签集中众数标签（摩尔投票 算法）
    :param labels:
    :return:
    '''
    vote = 0
    currentLabel = None
    for label in labels:
        if vote == 0:
            currentLabel = label
        elif currentLabel != label:
            vote -= 1
        else:
            vote += 1
    return currentLabel

def getClassifyAttr2(dataSet,labels,usedAttrs):
    '''
    寻找最佳分类属性，针对生成树有修改
    主要是保证，不能返回已经被使用于分类过的属性
    '''
    dataSetSize,totalAttribute = dataSet.shape
    totalEnt = getShannonEnt(labels)
    maxGain = float('-inf')
    maxGainAttrIdx = None
    for i in range(totalAttribute):
        attrGain = getGainForAttr(dataSet,i,labels,totalEnt)
        if attrGain > maxGain and i not in usedAttrs:
            maxGainAttrIdx = i
            maxGain = attrGain
    return maxGainAttrIdx

def createTree(dataSet,labels,usedAttrs):
    '''
        生成树。最终树的具体结构是{a: {v1: {}, v2:{}, v3:{} ...}}，其中a是某个分类属性，而v1,v2,v3是这个属性可能的取值。
        在每个取值下面是一个子集，借助这个子集和除了属性a之外另一个分类属性又可以生成一个树，如此递归。
        当然有些取值下面可能因为
        1. 训练集中这个分支下所有样本都属于同一类（叶节点值确定），
        2. 或者没有样本了（此时难以判断，干脆就以众数label作为结果），
        3. 或者是已经没有未使用的分类属性用于进一步分类这个子集（取子集中的众数label作为叶节点的值）
        结束递归
    '''
    if labels.count(labels[0]) == len(labels):  # 情况1
        return labels[0]
    if len(dataSet) == 0 or len(usedAttrs) == dataSet.shape[1]:  # 情况2 和 3
        return findPublicLabel(labels)

    attrIdx = getClassifyAttr2(dataSet,labels,usedAttrs)  # 计算当前最佳分类属性
    usedAttrs.append(attrIdx)  # 记录其已经使用的情况

    attrVals = set([row[attrIdx] for row in dataSet])
    # 如果只是为了看清树的结构，可以不用抽象的下标，而是一个字符串来表达某个分类属性，如resTree = {'attr[%s]' % attrIdx: {}}
    resTree = {attrIdx: {}}
    for val in attrVals:  # 针对attrIdx这个下标的属性（作为分类属性）的每个取值val
        subDataSet,subLabels = [],[]
        for i,row in enumerate(dataSet):  # 获取到子集的记录和子集的标签
            if row[attrIdx] == val:
                subDataSet.append(row)
                subLabels.append(labels[i])

        resTree[attrIdx][val] = createTree(array(subDataSet),subLabels,usedAttrs)  # 递归构造树

    return resTree  # 别忘了返回树，保证递归的自洽

def classify(inX, tree):
    '''
    构造完树之后还没有完，树只是模型，要把一个输入向量通过模型转化成一个预测分类结果才行
    函数不复杂，看某个向量某个属性的取值，这个取值能否直接判断出分类，不行地话递归判断即可。
    '''
    attrIdx = tree.keys()[0]
    attrVal = inX[attrIdx]
    if type(tree[attrIdx][attrVal]).__name__ == 'dict':
        # 如果是dict，说明输入向量的当前属性的值还不足以说明其具体应该属于什么分类，继续到下一层递归
        classify(inX, tree[attrIdx][attrVal])
    else:
        return tree[attrIdx][attrVal]


'''
==================================================================
'''
if __name__ == '__main__':
    dataSet = array([
        [0,0,0,0,0,0],
        [1,0,1,0,0,0],
        [1,0,0,0,0,0],
        [1,1,1,1,1,0],
        [2,2,2,0,2,1],
        [0,0,1,1,1,1]
    ])
    labels = [1,1,1,0,0,0]
    tree = createTree(dataSet, labels, [])
    print tree
    print classify([2,0,1,0,1,0],tree)