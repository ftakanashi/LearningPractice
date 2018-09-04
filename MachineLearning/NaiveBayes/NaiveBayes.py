# -*- coding:utf-8 -*-

'''
核心公式是概率论中的贝叶斯公式
并且基于假设，被分类对象各个属性间互相独立，因此可以将贝叶斯公式中的p{(x1,x2,x3...xn) | c}写成p{x1|c} * p{x2|c}...
针对每个属性分类ci，计算p{(x1,x2..xn)|ci} * p{ci}值中最大的那个，认为它就是待分类向量{x1,x2,...xn}的分类
从感觉上来看，一个向量最可能的分类归属，是这个分类本身在整体数据集上出现的概率 乘以 已知此分类中所有记录第n位上出现xn的概率
简单来说，1.某个分类占总体数据集比重越大，待分类向量越可能归属于它。极端情况全是一个分类，我们自然有理由认为待分类向量也属于这个分类
2. 某个分类中的向量第n个属性越容易出现xn，待分类向量越可能归属于它。极端情况一个分类下的第一个属性值都是待分类向量的第一个属性x1时，我们自然也有理由认为待分类向量归属于这个分类
'''

from collections import defaultdict
from numpy import where,array

def getLabelProb(labels):
    '''
    计算各个label的出现概率p{ci}
    :param labels:
    :return: 一个字典，key是label值，value是p{ci}
    '''
    count = defaultdict(int)
    total = len(labels)
    for label in set(labels):
        count[label] += 1
    res = {}
    for k,v in count.iteritems():
        res[k] = float(v) / total

    return res

def getAttrProb(dataSet, labels):
    '''
    获取每一种label分类中，每个向量的每个属性取值的概率p{xn|ci}
    :param dataSet:
    :param labels:
    :return: 返回结构比较复杂，是个嵌套字典
    嵌套字典的第一层key是label值，value是当前label分类下各个属性取值概率分布情况字典
    进入这个value字典后，它的key是属性下标值，value是当前分类，当前属性的取值概率分布字典
    再进入这个value字典后，它的key是当前属性的取值，value是当前分类，当前属性，当前取值的概率。对概率为0的取值不包含在数据结构中需注意
    '''
    categoryVals = set(labels)
    categories = {}
    for categoryVal in categoryVals:  # 将不同取值的记录分到不同key下的value中
        categories[categoryVal] = dataSet[where(labels == categoryVal)]

    def processRow(rows):
        '''
        辅助函数，计算一种分类下所有记录各个属性的取值，即p{xn|c}
        :param rows:
        :return:
        '''
        res = {}
        total = len(rows)
        for row in rows:
            for i,val in enumerate(row):
                if i not in res:
                    res[i] = {}
                if val not in res[i]:
                    res[i][val] = 1
                else:
                    res[i][val] += 1
        # 至此res中res[i][val]是当前分类所有记录中第i个属性取值val的个数
        for attr,valDis in res.iteritems():
            for val,count in valDis.iteritems():
                valDis[val] = float(count)/total  # 将个数全部除以总记录数，获取到p{xn|c}

        return res

    attrProb = {}
    for category,rows in categories.iteritems():  # 分类别分别计算各子数据集，然后统一放到attrProb数据结构中
        attrProb[category] = processRow(rows)

    return attrProb


def train(dataSet, labels):
    '''
    训练函数。实质上是计算得出了各个分类的各个属性的各个取值的概率分布
    :param dataSet:
    :param labels:
    :return:
    '''
    labelProb = getLabelProb(labels)
    attrProb = getAttrProb(dataSet,labels)
    model = (attrProb,labelProb)
    return model

def test(inX,model):
    '''
    测试函数。根据训练得到的概率分布，寻找可以让P{x1|ci}*P{x2|ci}...*P{xn|ci}*P{ci}最大的ci值，i是多少
    :param inX:
    :param model:
    :return:
    '''
    attrProb, labelProb = model
    # print attrProb
    maxc = float('-inf')
    est = None
    for label,pc in labelProb.iteritems():
        pwc = 1
        for i,attr in enumerate(inX):
            pwc *= attrProb[label][i].get(attr,0)
        currc = pc * pwc
        if currc > maxc:
            est = label

    return est

if __name__ == '__main__':
    model = train(array([[1,0,1,1],[1,1,0,0],[1,1,1,0],[0,1,0,0],[0,1,0,1]]), labels=array([1,1,0,2,0]))
    print test([0,0,0,0],model)

