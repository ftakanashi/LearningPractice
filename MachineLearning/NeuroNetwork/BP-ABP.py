# -*- coding:utf-8 -*-
from math import exp

from numpy import array
from random import random

def sigmoid(x):
    return exp(x) / (1 + exp(x))

class NeuroUnit:
    def __init__(self,w,x,threashold,output=None):
        '''
        :param w: 上一层到本神经元连接权 array类型
        :param x: 上一层的输出值 array类型，本神经元同层兄弟元可通用
        :param threashold:  本神经元阈值 float
        :param output:  本神经元输出 float
        :return:
        '''
        self.w = w
        self.x = x
        self.threashold = threashold
        if output is None:
            self.updateOutput()
        else:
            self.output = output

    def updateOutput(self):
        self.output = sigmoid((self.w * self.x).sum() - self.threashold)

    def __repr__(self):
        return '({}) => {}'.format(self.threashold, self.output)

class NeuroNetWork:
    '''
    神经网络模型
    '''
    def __init__(self,inputSize,outputSize,hiddenLayers):
        '''
        :param inputSize: 输入向量维数（隐层维数暂时默认和这个值一样）
        :param outputSize:  输出向量维数
        :param hiddenLayers:  隐层数量
        :return:
        '''
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.hiddenLayers = hiddenLayers

        # 初始化输入层
        firstLayer = array([NeuroUnit(None,None,0,0) for _i in range(self.inputSize)])
        self.net = [firstLayer,]
        lastLayerOutput = array([unit.output for unit in firstLayer])

        # 初始化隐层
        for _i in range(self.hiddenLayers):   # 每个隐层
            tmp = []
            for j in range(self.inputSize):  # 每个神经元
                lastLayerWeight = array([random() for _j in range(self.inputSize)])  # 随机初始化上一层到本神经元的连接权
                unit = NeuroUnit(lastLayerWeight, lastLayerOutput, random())
                tmp.append(unit)

            lastLayerOutput = array([unit.output for unit in tmp])
            self.net.append(tmp)

        # 初始化输出层
        outputLayer = [NeuroUnit(array([random() for _j in range(self.inputSize)]), lastLayerOutput, random()) for _i in range(self.outputSize)]
        self.net.append(outputLayer)

    def train(self,dataSet,labels,ita=0.1):
        '''
        基于BP算法的训练算法
        :param dataSet: 数据集
        :param labels: 数据集标签
        :param ita: 学习率
        :return:
        '''
        m,n = dataSet.shape
        round_count,total_count,sn = 0,0,0
        old_ey,ey = 0,0
        while True:
            round_count += 1
            for trainCount in range(m):  # 一次训练迭代
                total_count += 1

                for inputIdx,unit in enumerate(self.net[0]):    # 喂入一条训练集数据到输入层
                    unit.output = dataSet[trainCount][inputIdx]

                lastLayerOutput = array([u.output for u in self.net[0]])
                for layer in self.net[1:]:  # 从下至上，最终计算出本次迭代输出层数据
                    for unit in layer:
                        unit.x = lastLayerOutput
                        unit.updateOutput()
                        # ca = 0
                        # for k in range(n):
                        #     ca += unit.w[k] * unit.x[k]
                        # unit.output = sigmoid(ca - unit.threashold)
                    lastLayerOutput = array([u.output for u in layer])

                y_est = array([u.output for u in self.net[-1]])  # 本次迭代获得的估计值
                y = labels[trainCount]  # 实际值
                ey = 0.5 * ((y_est - y) ** 2).sum()  # 误差计算

                if abs(old_ey - ey) < 0.01:    # 资料上说0.0001，不过发现0.0001对于自建网络 && Python CPU环境学习效率很低，必须降低到0.01才能比较快出结果
                    sn += 1
                    if sn == 100:    # 必须连续一百次迭代的误差都小于0.0001，才认为学习完成
                        print total_count, round_count
                        return
                else:
                    old_ey = ey
                    sn = 0

                # 先计算输出层的梯度项的值
                g = []
                for j in range(self.outputSize):
                    g.append(y_est[j] * (1 - y_est[j]) * (y[j] - y_est[j]))
                g = array(g)

                # 再计算各个隐层梯度项的值
                hidden_eh = []
                lastLayerEh = g
                lc = len(self.net) - 2
                while lc > 0:    # 一个隐层中
                    layer = self.net[lc]
                    eh = []
                    for h in range(self.inputSize):    # 每个神经元
                        out = layer[h].output
                        w_from = array([unit.w[h] for unit in self.net[lc+1]])
                        eh.append(out * (1 - out) * ((w_from * lastLayerEh).sum()))
                    hidden_eh.append(eh)
                    lastLayerEh = array(eh)
                    lc -= 1

                # 更新隐层的连接权和阈值
                for i in range(self.hiddenLayers):
                    layer = self.net[i+1]  # net[0]是输入层
                    for j,unit in enumerate(layer):
                        unit.w = unit.w + hidden_eh[i][j] * unit.x * ita
                        unit.threashold = unit.threashold - ita * hidden_eh[i][j]

                # 更新输出层的连接权和阈值
                for j,unit in enumerate(self.net[-1]):
                    unit.w = unit.w + unit.x * g[j] * ita
                    unit.threashold = unit.threashold - ita * g[j]

    def test(self,vector):
        '''
        :param vector: 待测试向量，array类型
        :return:
        '''
        for i,unit in enumerate(self.net[0]):
            unit.output = vector[i]
        lastLayerOutput = vector
        for layer in self.net[1:]:    # 对隐层和输出层进行计算
            for unit in layer:
                unit.x = lastLayerOutput
                unit.updateOutput()
            lastLayerOutput = [u.output for u in layer]  # 更新当前隐层的总输出

        return ','.join([str(unit.output) for unit in self.net[-1]])   # 返回输出层
'''
ABP算法的各个计算小模块和BP算法类似，只不过在框架安排上不太一样。

从方法论的角度来说，BP算法首先是算出某一次迭代的得到的估计值，利用估计值和实际值计算出误差值ey作为训练是否结束的判断标准，
如果要继续学习，那么就以本次得到的估计值和实际值作为基础，去计算并更新参数。

而ABP是将一轮迭代得到的所有估计值和实际值通过更高维的数据结构保存，并以此计算出来的训练集误差值总和eys（称为累积误差）作为训练是否结束的标准，
如果需要继续学习，那就以本轮最后一个（存疑）记录的相关数据来计算，并更新参数

具体ABP算法不实现出来了，不过可以看出，ABP比BP粒度更大，因此其学习效率更高，可接受的结束学习标准比如sn也可以设置一个更小的阈值
不过由于其粗放的特点，在误差下降到一定程度之后就很难再进一步地下降，这也是需要考虑的一点。
'''

if __name__ == '__main__':
    net = NeuroNetWork(8,1,1)
    dataSet = array([array([ 0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.697,  0.46 ,  0.   ]), array([ 1.   ,  0.   ,  1.   ,  0.   ,  0.   ,  0.   ,  0.774,  0.376,  0.   ]), array([ 1.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.634,  0.264,  0.   ]), array([ 0.   ,  0.   ,  1.   ,  0.   ,  0.   ,  0.   ,  0.608,  0.318,  0.   ]), array([ 2.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.556,  0.215,  0.   ]), array([ 0.   ,  1.   ,  0.   ,  0.   ,  1.   ,  1.   ,  0.403,  0.237,  0.   ]), array([ 1.   ,  1.   ,  0.   ,  1.   ,  1.   ,  1.   ,  0.481,  0.149,  0.   ]), array([ 1.   ,  1.   ,  0.   ,  0.   ,  1.   ,  0.   ,  0.437,  0.211,  0.   ]), array([ 1.   ,  1.   ,  1.   ,  1.   ,  1.   ,  0.   ,  0.666,  0.091,  1.   ]), array([ 0.   ,  2.   ,  2.   ,  0.   ,  2.   ,  1.   ,  0.243,  0.267,  1.   ]), array([ 2.   ,  2.   ,  2.   ,  2.   ,  2.   ,  0.   ,  0.245,  0.057,  1.   ]), array([ 2.   ,  0.   ,  0.   ,  2.   ,  2.   ,  1.   ,  0.343,  0.099,  1.   ]), array([ 0.   ,  1.   ,  0.   ,  1.   ,  0.   ,  0.   ,  0.639,  0.161,  1.   ]), array([ 2.   ,  1.   ,  1.   ,  1.   ,  0.   ,  0.   ,  0.657,  0.198,  1.   ]), array([ 1.  ,  1.  ,  0.  ,  0.  ,  1.  ,  1.  ,  0.36,  0.37,  1.  ]), array([ 2.   ,  0.   ,  0.   ,  2.   ,  2.   ,  0.   ,  0.593,  0.042,  1.   ]), array([ 0.   ,  0.   ,  1.   ,  1.   ,  1.   ,  0.   ,  0.719,  0.103,  1.   ])])
    realDataSet = dataSet[:,:-1]
    labels = []
    # labels = [(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),
    #           (0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),]
    for label in dataSet[:,-1]:
        labels.append(array([label]))
    labels = array(labels)
    net.train(realDataSet,labels,ita=0.1)
    raw_input('Train Over')
    for rec in dataSet[:,:-1]:
        print net.test(rec)