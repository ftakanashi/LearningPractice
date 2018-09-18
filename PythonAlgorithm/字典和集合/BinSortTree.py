# -*- coding:utf-8 -*-

'''
二叉搜索树是一种递归满足：所有左子树的元素值（或关键码对应的元素值）都小于根节点，所有右子树的元素值（或关键码对应的元素值）都大于根节点
对一颗二叉搜索树进行中根序遍历可得到一个不递减的序列
由于仅仅知道一个中根序列是不足以推出原树形状的（如果再知道前跟序列或者后跟序列就可以了），所以一个数据集的二叉搜索树不唯一
'''
class BinTNode:
    def __init__(self,data,left=None,right=None,parent=None,type=None):
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent
        self.type = None

    def __lt__(self, other):
        return self.data < other.data

    def __le__(self, other):
        return self.data < other.data

    def left(self):
        return self.left

    def right(self):
        return self.right

    def data(self):
        return self.data

    def parent(self):
        return self.parent

    def type(self):
        return self.type
class Assoc:
    def __init__(self,key,value):
        self.key = key
        self.value = value

    def __lt__(self, other):
        return self.key < other.key

    def __le__(self, other):
        return self.key <= other.key

    def __str__(self):
        return 'Assoc({0},{1})'.format(self.key,self.value)

'''
采用二叉树时定义的BinTNode作为载体来构造二叉搜索树
'''

class DictBinTree:
    def __init__(self):
        self._root = None

    def is_empty(self):
        return self._root is None

    def search(self,key):
        bt = self._root
        while bt is not None:
            entry = bt.data    # entry是某个树的根节点中的值，而作为一个代替字典类型的二叉搜索树，这个值是一个k-v对
            if key < entry.key:
                bt = bt.left
            elif key > entry.key:
                bt = bt.right
            else:
                return entry.value

        return None

    def insert(self,key,value):
        '''
        插入一个数据，根据提供的新数据的key左右判断，碰到相同的key时用新value替换老value
        插入数据一定是将数据作为一个新的叶节点加入到树中
        :param key:
        :param value:
        :return:
        '''
        bt = self._root
        if bt is None:
            self._root = BinTNode(Assoc(key,value))
            return
        while True:
            entry = bt.data
            if key < entry.key:
                if bt.left is None:
                    bt.left = BinTNode(Assoc(key,value))
                    return
                bt = bt.left
            elif key > entry.key:
                if bt.right is None:
                    bt.right = BinTNode(Assoc(key,value))
                    return
                bt = bt.right
            else:
                bt.data.value = value
                return

    def values(self):
        '''
        中根序遍历配合生成器，留出了一个顺序遍历接口
        yield的时候不应该返回Assoc类对象。因为一旦把这个对象给了用户，你不确定用户会对其做什么修改，
        如果修改了value可能会导致原二叉搜索树的崩坏
        :return:
        '''
        from Queue import LifoQueue as Stack
        stack = Stack()
        bt = self._root
        stack.put(bt)

        while not stack.empty():
            while bt.left is not None:
                stack.put(bt)
                bt = bt.left
            yield bt.data.value
            bt = stack.get()
            yield bt.data.value
            bt = bt.right

    def delete(self,key):
        '''
        删除二叉搜索树中的指定键的键值对
        :param key:
        :return:
        '''
        p,q = None,self._root
        while q is not None and q.data.key != key:
            # 始终保持p是q的父节点
            p = q
            if key < q.data.key:
                q = q.left
            else:
                q = q.right
        if q is None:
            # 没有找到相应的key，无需删除
            return False

        # 到这里为止，q就是键是key的那个元素。要删除q这个节点，分成两种情况讨论。即q最多只有一个子树和q有两个子树的情况。
        # 下面以q有无左子树作为条件进行条件的判断。
        if q.left is None:
            # 没有左子树的情况，只需要考虑q的右子树何去何从
            if p is None:
                # q是根节点情况
                self._root = q.right
            if q is p.left:
                # q本来是p的左子树，将q的右子树作为p的左子树接上
                p.left = q.right
            elif q is p.right:
                # q本来是p的右子树，将q的右子树作为p的右子树接上
                p.right = q.right

        else:
            # q有左子树的情况，
            r = q.left
            while r.right is not None:
                # 找到q左子树最右下角，即q左子树中最大的位置，将q的右子树作为这个位置的右子树接上
                r = r.right
            r.right = q.right

            # 这里和上面没有左子树的情况类似了，无非是操作对象由q.right变成q.left。
            if p is None:
                self._root = q.left
            elif q is p.left:
                p.left = q.left
            elif q is p.right:
                p.right = q.left

'''
二叉搜索树的使用面临一个问题，如果树的构建过于“偏”，会导致搜索树失去其搜索的优越性，而变成了线性的结构
因此构造二叉搜索树存在一个“最佳”的问题。为了找到一个最佳二叉搜索树的结构，需要用一个指标来衡量检索效率
从使用的角度来看，二叉搜索树的检索效率主要和树的形状以及特定值检索频率有关。另外，检索可以分成“成功检索”和“失败检索”两种
前者值找的值恰好是树中节点，后者则相反。为了统一两者，可将任意二叉搜索树扩充成一个扩充二叉树，其外部节点用可能落到该节点下的所有值的范围组成。
于是我们就可以导出检索效率的公式E(n) = sum(pi*(li+1)) + sum(pj*(lj))，其中pi指各内部节点的检索概率，li指它所在的层数。
由于确定某个值是内部结点的值最后还有一次判等的操作，因此共需要li+1次判断。另一方面，pj指各个外部节点的检索概率，lj指外部节点所在层数，这里不用+1
'''
'''
最简单的情况，如果在有限的取值范围（比如n个值）内，检索概率呈均匀分布
可以推得E(n) = （2 * IPL + 3n) / (2n + 1)
IPL = sum(log(2,k))，k从1开始取值到n。IPL称最小检索长度。显然IPL越小E(n)越小，二叉搜索树的检索效率就越好。而IPL最小意味着树最矮
对于构造这样的二叉搜索树，只要将中位数作为根节点，然后根据其他数和中位数之间的大小关系构建左子树和右子树即可
'''
class DictOptBinTree(DictBinTree):
    '''
    简单最佳二叉搜索树类的构建。需要注意，如果使用了一般二叉搜索树类中定义的增删方法，
    由于那些方法不保证最佳搜索树的最佳性，所以越用树的形状可能会越差
    '''
    def __init__(self,seq):
        DictBinTree.__init__(self)
        data = sorted(seq)
        self._root = DictOptBinTree.buildOBT(data,0,len(data)-1)

    @staticmethod
    def buildOBT(data,left,right):
        if left > right:
            return
        mid = (left + right) // 2
        leftChild = DictOptBinTree.buildOBT(data,left,mid-1)
        rightChild = DictOptBinTree.buildOBT(data,mid+1,right)
        return BinTNode(Assoc(*data[mid]),leftChild,rightChild)

'''
对于一般的最佳二叉排序树，其实就是要找到一个树的整体带权路径长度最小的结构。这很容易让我们联想到哈夫曼算法
哈夫曼算法的输入是一个权值序列，而构造出来的哈夫曼树是把这个序列作为外部节点的树。
构建最佳排序树算法输入是一个权值&值序列，构造出的树中这些序列中的元素是作为内部节点存在的。
构建【最佳】二叉排序树的算法比较复杂，简单说明一下：
首先明确几个表示法。T(i,j)表示由内部结点vi,v(i+1)....v(j-1)以及外部节点ei,...ej构成的一棵排序树。我们的目标就是求出T(0,n)的最佳形态
W(i,j)表示T(i,j)中所有节点的权值的和，C(i,j)表示T(i,j)处于最佳形态时的带权路径长度。
利用DP思想，可以写出这样一个状态转移方程：
C(i,j) = W(i,j) + min(C(i,k) + C(k+1,j))；其中 i <= k < j，取特定k的时候表示构造出来的这个T(i,j)树以vk内部结点作为根节点构造
自然，让等式右边后半部分取到最小值的那个k，就是最终最优二叉搜索树的根节点的vk编号
另外，起始条件可以看做C(i,i) = 0，则我们可以知道由一个内部结点和两个外部节点构成的最基本的最优二叉搜索树可以这样来表示
C(n,n+1) = W(n,n+1) + min(C(n,n) + C(n+1,n+1))，后半部分等于0，而前半W(n,n+1) = vn的权值 + en的权值 + e(n+1)的权值，相当于三个节点的权值单纯相加
通过上面这个状态转移方程，可以通过构造几个二维数组（分别要来保存W，C，下标等信息）来构造算法
最终算法的输入是一些作为内部节点的权值和作为外部节点的权值，而得到的是东西中可以分析出这些权值能构成的最佳二叉搜索树
'''
