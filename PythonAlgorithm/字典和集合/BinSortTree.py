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

