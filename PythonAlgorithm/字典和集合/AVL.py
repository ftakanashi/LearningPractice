# -*- coding:utf-8 -*-

'''
AVL树是一种特别的二叉搜索树，每个节点额外保存一个bf（Balance Factor）值来记录此节点左子树高度减去右子树高度的差。
并且AVL保证所有节点中的BF值的取值只能是-1,1或0。这也就是说，任何成对的左右子树高度差绝对值都不超过1。
所以AVL树也是递归的，即AVL树的所有子树也都是AVL树
由于AVL树本身是二叉搜索树的一种，所以检索方面和普通二叉搜索树一样。不同的地方在于AVL树的插入和删除操作，还要伴随着一些局部的调整
保证BF值的取值，从而保证了增删操作不会对搜索树的平衡性有很大影响。AVL树也称平衡二叉树
'''
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

class AVLNode:
    ''' AVL树节点类 '''
    def __init__(self,data,left=None,right=None):
        self.data = data
        self.left = left
        self.right = right
        self.bf = 0

'''
一些需要明确的事情：
由于AVL节点的bf值取值可能是-1,0,1三种。我们定义“非平衡”状态指bf != 0的状态，而“失衡”状态指bf<-1或bf>1的情况
'''

class DictAVL:
    def __init__(self):
        self._root = None

    @staticmethod
    def LL(a,b):
        '''
        LL变换，新插入节点在左子树的左子树，RR，LR,RL变换也都类似。
        这些变换方法并不是说将失衡的树重新变平衡，而是做的一个局部的改变，要做到重新平衡，还需要在方法外面将原来父节点连接上经过变换后新的局部的根节点
        因此这些方法最终都要返回经过变换之后，新的根节点是什么
        '''
        a.left = b.right
        b.right = a
        a.bf = b.bf = 0
        return b

    @staticmethod
    def RR(a,b):
        a.right = b.left
        b.left = a
        a.bf = b.bf = 0
        return b

    @staticmethod
    def LR(a,b):
        c = b.right
        a.left,b.right = c.right,c.left
        c.left,c.right = b,a
        if c.bf == 0:
            a.bf = b.bf = 0
        elif c.bf == 1:
            a.bf = -1
            b.bf = 0
        elif c.bf == 1:
            a.bf = 0
            b.bf = 1
        c.bf = 0
        return c

    @staticmethod
    def RL(a,b):
        c = b.left
        a.right,b.left = c.left,c.right
        if c.bf == 0:
            a.bf = b.bf = 0
        elif c.bf == 1:
            a.bf = 0
            b.bf = -1
        elif c.bf == -1:
            a.bf = 1
            b.bf = 0
        c.bf = 0
        return c

    '''
    现在我们来看一下如何实现AVL树的插入操作。
    插入操作其实大概地分成两个部分，第一部分是我们定位一个合适的地方去将新节点append上去；第二部分是检查append上之后，树是否失衡
    如果发生了失衡情况，则需要应用上面的LL/RR/LR/RL四种变换方法将树重新置平衡。
    由于AVL树的递归性质，判断一个树是否失衡，很重要的一点是关注“最小非平衡子树”,即插入新节点后从根节点开始到新节点为止路径上最靠近叶节点的，bf不为0的子树
    只要这个子树恢复平衡，那么整体树就都恢复平衡了。
    有时，这样的树并不存在，即从根节点到新节点路径上所有的bf都是0的情况。此时只要根据新节点的位置，依次更新这些0为-1或1即可
    如果找到了最小非平衡子树，我们令其为a吧。由于a的定义，所以a到新节点的路径上（不包括a本身）所有节点目前的bf=0，根据路径方向，要将这些bf更新为-1或1
    更新完了之后，需要检查a是否失衡了。根据新节点插入在a的左子树还是右子树，以及a原来的a.bf值，可以分成四种情况讨论：
        1. a.bf = 1  &&  新节点位于a.left
        2. a.bf = 1  &&  新节点位于a.right
        3. a.bf = -1 &&  新节点位于a.left
        4. a.bf = -1 &&  新节点位于a.right
    针对四种情况分别的解决方案是：
        1.
          1.1 新节点位于a.left.left，做LL调整
          1.2 新节点位于a.left.right，做LR调整
        2. a未失衡，而且恢复了平衡，a.bf置0
        3. a未失衡，而且恢复了平衡，a.bf置0
        4.
          4.1 新节点位于a.right.right，做RR调整
          4.2 新节点位于a.right.left，做RL调整

    '''

    def insert(self,key,value):
        a = p = self._root    # a用来找最小非平衡子树，p作为扫描a到新节点之间的游标
        if a is None:
            self._root = AVLNode(Assoc(key,value))
            return
        pa = q = None    # pa,q分别表示a,p的父节点，这点在循环中保持不变。记录q的原因和一般二叉搜索树做insert记录q原因一样，是为了能够方便地新增节点
        # 记录pa则是为了万一要发生树形态的变换，可以方便的找到变换树的父节点，重新链接过去。

        while p is not None:
            '''这个循环是以p为游标先行，并且根据新插入的key和value去寻找合适的插入位置
            寻找的过程中顺便关注bf值，从而更新a的记录，确定根节点到插入位置的路径上，最小非平衡子树在哪里
            '''
            if key == p.data.key:    # 对已经存在的key直接更新
                p.data.value = value
                return
            if p.bf != 0:    # 如果发现p是非平衡子树，那么最小非平衡子树更新为p上面来
                pa,a = q,p
            q = p
            if key < p.data.key:
                p = p.left
            else:
                p = p.right

        # 这个循环结束之后，q应该是待插入新节点的父节点，而p是None，后续还可以作为游标被重新赋值
        node = AVLNode(Assoc(key,value))
        if key < q.data.key:
            q.left = node
        else:
            q.right = node

        # 新节点插入结束，接下来开始检查最小非平衡子树的失衡情况。
        # 不过在那之前可以先更新掉a到新节点间所有bf是0的节点的bf值，因为无论需不需要转换，这些值都是要更新的，而且这些值不会因为转换而改变

        # 先判断一下新节点在最小非平衡子树的左还是右子树中
        if key < a.data.key:
            p = b = a.left  # 新节点位于最小非平衡子树的左子树
        else:
            p = b = a.right  # 新节点位于最小非平衡子树的右子树
        # 这里除了p还赋值了一个b。一来p是游标，下面循环中p会变化，从而就无法表名新节点的左右。二来，如果后续需要做变换，b也可直接拿来用
        while p is not node:
            '''这个循环用来更新a中新节点所在左或右子树的根节点 到 新节点的父节点为止所有节点的bf值
            之前这些bf值都是0（根据a的定义），因此可以直接一个比较然后赋值为-1或1
            '''
            if key < p.data.key:
                p.bf = 1
                p = p.left
            else:
                p.bf = -1
                p = p.right
        # 这个循环完成后，最小非平衡子树a出发到新节点路径上所有原先bf是0的节点bf都得到了更新

        if b is a.left and a.bf in (0,-1):    # 新节点在左子树，而左子树不是较高的子树，那么不失衡，简单改变a.bf即可
            a.bf += 1
            return
        if b is a.right and a.bf in (0,1):    # 同上
            a.bf -= 1
            return

        # 如果程序能运行到这里，说明新插入节点插入了a中较高的子树，导致失衡了，因此需要变换
        if b is a.left:    # 新节点在a的左子树
            if b.bf == 1:   # 新节点在a的左子树的左子树，此时b的bf已经在上面循环中更新过了，所以可以用来判断新节点位于b的左右子树情况
                b = DictAVL.LL(a,b)
            else:
                b = DictAVL.LR(a,b)
        else:                        # 新节点在a的右子树
            if b.bf == -1:
                b = DictAVL.RR(a,b)
            else:
                b = DictAVL.RL(a,b)
        # 至此，b中保存的树结构已经是一个“优化后平衡的”树结构了，接下来只要考虑如何将此树整合回原树即可

        if pa is None:    # 说明a就是原树，因此根节点self._root需要变更
            self._root = b
        else:
            if a is pa.left:
                pa.left = b
            else:
                pa.right = b
    '''
    总结一下，AVL树插入操作大致分成下面几个步骤：
    1. 通过p,a两个游标先后行，遍历树。p是为了找到新加入节点的位置，a是为了找到最小非平衡子树
    2. 插入节点
    3. 确定新节点位于最小非平衡子树的左子树还是右子树，以及a.bf的取值。根据前者可更新a到新节点之间所有节点的bf值（原来是0）
    4. 根据3中获得的左/右以及原a.bf两个信息，再来尝试更新a.bf。左或右两种取值，a.bf三种取值共六种情况中，有四种情况可以直接修改a.bf而不改变树结构
       剩余两种情况，还根据b的左子树/右子树各分成两个情况，相当于四个小情况。每个小情况都对应一种变换方式（LL,RR,LR,RL）

    最后，需要指出，这个插入算法的时间和空间复杂度都是O(logn)，很快
    '''

if __name__ == '__main__':
    avl = DictAVL()
    import string
    import random
    a,b = range(1,10),list(string.lowercase)
    random.shuffle(a)
    random.shuffle(b)
    pool = zip(a,b[:9])
    print pool

    for k,v in pool:
        avl.insert(k,v)
        print avl._root.data
