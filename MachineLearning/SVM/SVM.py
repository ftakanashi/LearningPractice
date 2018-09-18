# -*- coding:utf-8 -*-

'''
SVM全称Support Vector Machine。据说是最好的现成的分类器。
SVM有很多种实现，其中最流行的一种是基于SMO（序列最小优化，Sequence Minimal Optimization）算法。
然后通过核函数可以将一个SVM给泛化到各种不同的数据集中
'''

'''
线性可分：
如果一个集合可以由一个超平面分成两部分，一类值在超平面的一边，另一类再另外一边，没有串的情况，那么这个集合就是线性可分的
所谓超平面，是指N维空间中N-1维的东西，比如平面上的超平面就是直线
对于一个线性可分的集合，如果要找到一个最适合分割它的超平面，一个办法就是要尽量让所有靠近边界的点都远离超平面。

首先我们要知道如何计算一个点到一个超平面的距离。以三维空间为例，点面距公式是abs(Ax+By+Cz+D)/sqrt(A^2+B^2+C^2)
类比到N维空间中，那么这个公式可以写成 (w*x+b)/L2(w)，其中w和x是两个N维向量，b可以看做是截距项。易知(w,b)决定了一个超平面
L2(w)被称为w的L2范数，也可以写成||w||，意思就是w中各维度量的平方和再开方，如点面距公式中的那个一样。
这里还有一个问题，如果w*x+b的值是负，那么距离就变成了负值。
我们可以定义一个二分类问题的分类标签是1和-1，如此构建一个y*(w*x+b)这样一个值就是永远都是正的了，
而且在标签分类正确时距离超平面越远（无论是在哪一侧），这个值越大。这个值被称为函数间距。构造函数间距的另一个好处是，
在二分类问题中，一个样本如果通过w*x+b算出来是正，但实际上其标签y是-1，这样其到超平面的距离在计算上成为负数。这个负数实际上表明
当前超平面的选择很不好。也就是说，函数间距可以用来表征超平面分类的正确性。

函数间距还有一个特点，就是当w和b被同比缩放的时候，间距值也会同比缩放。为了能够得到规范的一个指标，可以再除以L2(w)
除完后得到的规范的指标称为几何间距。从几何的意义上来说，在预测正确的情况下这也是点到超平面真实的距离值。
函数间距这个“可变动”的特点在后面的处理中还会带来一些方便。

硬间隔最大化：
对于一个线性可分的样本空间，从直觉上我们可以感觉到，一个最佳的分类超平面，应该要满足样本集中所有点到其几何距离尽量大（尤其是靠近分类边界的那些点）
而可以证明这样做是合理的：定义超平面到样本集的几何距离为min(γi)，其中γi是指所有点到超平面的几何距离。
要求出来的，是样本集中，“所有点到超平面的几何距离最小值” 的最大值。这句话可能有点拗口，引号中的意思，其实就是说
距离超平面最近的点（可能不止一个）到超平面的距离，这个值根据w,b变化而不同，这本身也是一个函数。而寻求其获得最大值时的w,b，这就是我们要做的。

换句话说，这个过程是求一个函数在有限制的情况下的极值。用朗格朗日数乘法构造方程即可。不过在那之前我们还可以做一些优化
刚才提到过，函数间距和几何间距之间只相差一个L2(w)，而函数间距具有“可变动”的特征。对于同一个超平面，合法的表达有无数种，他们之间的关系就是w,b以及成比例，只要求出一对w,b即可
而不同表达方式下超平面算出的函数间距也是成比例的。那不妨令函数间距为1，求出函数间距最小值始终是1时w,b的值，然后用它来表示超平面
最终我们要解决的问题描述如下：

要求出(w,b)，使得1/L2(w)最大，并且任意样本集中的xi,yi满足yi(w*xi+b) >= 1。
L2(w)带有根号并且处于分母，不太容易处理，不妨将问题变换成求出w,b，使得L2(w)^2/2最小，并且.....（后面条件不变，除以2是为了后续求导方便）
将求最大问题改为了求最小问题
下面关注一下问题的后半部分中的不等式。当不等式取到等号的时候，此时的xi应恰好距离超平面的函数间距是1，换句话说，取到等号时的xi,yi
就是所谓的距离超平面最近的那些点。  我们把这些点的向量xi（也就是它的各个坐标们）成为“支持向量”

可以看出，决定最佳超平面的，和样本集中大多数样本无关，只和支持向量有关。
'''

'''
那么具体要怎么求出最佳分类超平面的w*和b*呢。这里涉及到比较复杂的数学过程。简单概括来说，就是将上面的这个有条件的求最值问题
先转化为一个拉格朗日方程（带有不等式条件的拉格朗日求最值问题），如 L(w,b,α)，其中α是一个向量，其各个分量分别去乘以各个样本的函数间距
然后使用拉格朗日对偶规则，将其转化为另一个形式。通过其可以求出α最优值α*。
之后就可以根据原始问题的KKT条件，代回，得到w*和b*的表达式。
//上面的公式比较难打，参看李航《统计学习方法》P105前后
'''

'''
下面介绍所谓的SMO算法。根据上面的推导可以知道，要求出最优超平面的w和b，可以先求出基于其拉格朗日函数L(w,b,α)的对偶问题的α，
并且由拉格朗日对偶性可以得到w,b和α之间的关系，因此就可以求解w和b了。
SMO算法的目标就是根据训练集数据，以及惩罚参数、容错参数等数据，找出这个数据集上对应的α和b
具体来说，SMO算法计算α的标准是找到一组符合本问题朗格朗日方程KKT条件的一组解。当α中所有分量都满足了KKT条件，这个最优化问题自然就解决了
但是一下让α这个N维向量（N是样本数量）满足KKT条件有些无理,所以SMO算法采用的办法是不断从α中选出两个分量αi和αj，对它们进行所谓“优化处理”使它们都逼近符合KKT条件
所有分量都经过这样的处理之后，自然就可以得到正确的解的α了。

如此，SMO算法要解决的就是两个问题，1. 如何找出合适的两个分量αi和αj；2. 优化处理具体如何做。
首先先来解答第二个问题。由于只研究αi和αj，其余的量都视为常量，所以原拉格朗日函数可以写成一个仅有αj表示的式子。再加上一些限定条件，相当于要做的，是在限定条件时求函数最值
于是这里就逃不开求导，令导数为0，研究定义域这几步。详细的不展开了，看书。这个过程中涉及到yi,yj不同/相同取值时上下界不同，以及上下界和导数为0的点之间取谁做最值等问题。这里面其实还蛮复杂的。
总之最终可以推导出一个αj(new) = αj(old) + xxx 或者 αj=High 或者 αj=Low 的迭代更新式子。另外的αi，则可以根据限制条件中的一条，通过αj的新老取值以及αi的老取值算出。
优化过后的αi和αj必然都是符合KKT条件的，因此可以根据两者取值看出相应的向量是否是支持向量。
另外根据“最终产物公式”w*和b*的公式，也可以算出在优化过αi和αj之后b的变化情况。虽然不太清楚为什么，但是这个b每次优化两个参数后都要更新。
如此不断地迭代更新α各个分量，直到误差较小，各分量收敛，训练结束。返回出α即可

至于第一个问题，暂不做说明，下面先实现一个简易版的SMO算法。简易的地方就是对第一个问题的处理。我们不严格去找合适的αi和αj，而是先找一个需要优化的αi，另一个αj则从剩余分量中随机选择
下文中的selectJrand和clipAlpha是两个辅助函数，然后我们构建了一个简化版本的SMO算法实现。
'''
from numpy import mat,zeros,multiply
import random
def selectJrand(i,m):
    j = i
    while j == i:
        j = int(random.uniform(0,m))
    return j

def clipAlpha(alphaJ, H, L):
    if alphaJ > H:
        alphaJ = H
    if alphaJ < L:
        alphaJ = L
    return alphaJ

def simpleSMO(dataMataIn,classLabels,C,toler,maxIter):
    dataMatrix = mat(dataMataIn)
    labelMat = mat(classLabels).transpose()
    b = 0
    m,n = dataMatrix.shape
    alphas = mat(zeros((m,1)))
    iter = 0
    while iter < maxIter:
        alphaPairsChanged = 0
        for i in range(m):
            fXi = float(multiply(alphas,labelMat).T * (dataMatrix * dataMatrix[i,:].T)) + b    # 第一个样本向量的估计值
            Ei = fXi - float(labelMat[i])    # 第一个样本向量的偏差值
            if ( labelMat[i] * Ei < -toler and alphas[i] < C ) or ( labelMat[i] * Ei > toler and alphas[i] > 0 ):    # TODO 这里还不是很懂为什么条件这么写
                # 仅alphas[i]不符合KKT条件需要优化时，选择alphas[i]作为第一个要进行调整的分量
                j = selectJrand(i,m)    # 简化就简化在这里，随机选第二个要进行调整的分量，而不是理性分析出第二个分量应该选择什么
                fXj = float(multiply(alphas,labelMat).T * (dataMatrix * dataMatrix[j,:].T)) + b
                Ej = fXj - float(labelMat[j])

                # 记录老的αi和αj，用于后续的比较。
                alphaIold = alphas[i].copy()
                alphaJold = alphas[j].copy()

                # 根据选择的两个样本的标签是否一致来决定上下界各是多少
                if labelMat[i] != labelMat[j]:
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, C + alphas[j] + alphas[i])
                if L == H:
                    print 'L == H'
                    continue

                # 计算η参数
                eta = 2.0 * dataMatrix[i,:] * dataMatrix[j,:].T - dataMatrix[i,:] * dataMatrix[i,:].T - dataMatrix[j,:] * dataMatrix[j,:].T
                if eta >= 0:
                    print 'eta >= 0'
                    continue
                alphas[j] -= labelMat[j] * (Ei - Ej) / eta    # 没有0<=α<=C的限制时αj的最优值
                alphas[j] = clipAlpha(alphas[j],H,L)    # 考虑 0<=α<=C 限制后的最优值
                if abs(alphas[j] - alphaJold) < 0.0001:    # αj的变化太小
                    print 'j not moving enough'
                    continue
                alphas[i] += labelMat[j] * labelMat[i] * (alphaJold - alphas[j])  # 根据αj结果计算新的αi

                # 根据新αi和αj值
                b1 = b - Ei - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i,:] * dataMatrix[i,:].T - \
                    labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[i,:] * dataMatrix[j,:].T
                b2 = b - Ej - labelMat[j] * (alphas[i] - alphaIold) * dataMatrix[i,:] * dataMatrix[j,:].T - \
                    labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[j,:] * dataMatrix[j,:].T
                if alphas[i] > 0 and alphas[i] < C:
                    b = b1
                elif alphas[j] > 0 and alphas[j] < C:
                    b = b2
                else:
                    b = (b1 + b2) / 2.0

                alphaPairsChanged += 1
                print 'iter: %d, i: %d, pairs changed: %d' % (iter, i, alphaPairsChanged)

        if alphaPairsChanged == 0:
            iter += 1
        else:
            iter = 0
        print 'iteration number: %d' % iter
    return b,alphas

'''
正如上面所说，简易版的SMO算法中并没有对需要优化的α分量做出理性判断，
而实际上，可以采取最大步长的策略来寻找第二个分量。所谓最大步长，就是希望优化后αj能够有尽量大的变化。这种思想也被称为启发式
而前面提到过的αj的迭代公式中，一个重要的参数是|Ei-Ej|，其中Ei，Ej分别是当前αi和αj根据当前SVM计算出的各自样本的wxk+b与实际值yk之间的误差
只要让|Ei - Ej|尽量大，我们就认为这是一个合理的αj的选择。
'''

class optStruct:
    def __init__(self, dataMatIn, classLabels, C, toler):
        self.X = dataMatIn
        self.labelMat = classLabels
        self.C = C
        self.tol = toler
        self.m = dataMatIn.shape[0]()
        self.alphas = mat(zeros((self.m,1)))
        self.b = 0
        self.eCache = mat(zeros((self.m,2)))

    def calcEk(self, oS, k):
        fXk = float(multiply(oS.alphas,oS.labelMat).T * (oS.X * oS.X[k,:]).T) + oS.b
        Ek = fXk - float(oS.labelMat[k])
        return Ek
