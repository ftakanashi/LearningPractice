# -*- coding:utf-8 -*-
import sys
import Queue
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

class BinTree:
    def __init__(self,root=None):
        self.root = root
        if not root:
            self._elems = []
        else:
            self._elems = list(self.flattenNodes(self.root))

    def flattenNodes(self,root):
        for node in self.horizIter():
            yield node.data

    def getRootNode(self):
        return self.root
    def setRootNode(self,node):
        self.root = node

    def getLeftNode(self):
        return self.root.left
    def getLeftChild(self):
        return BinTree(self.root.left)

    def getRightNode(self):
        return self.root.right
    def getRightChild(self):
        return BinTree(self.root.right)

    def horizIter(self):
        '''
        宽度优先遍历，返回BinTNode类的生成器
        :return:
        '''
        stack = Queue.Queue()
        stack.put(self.root)
        while not stack.empty():
            t = stack.get()
            if t.left is not None:
                stack.put(t.left)
            if t.right is not None:
                stack.put(t.right)
            yield t

    def preorderIter(self):
        '''
        先根序遍历节点，返回是BinTNode对象的生成器
        :return:
        '''
        rootNode = self.root
        if rootNode is None:
            return
        yield rootNode
        for leftChild in self.getLeftChild().preorderIter():
            yield leftChild
        for rightChild in self.getRightChild().preorderIter():
            yield rightChild

class FullBinTree(BinTree):
    '''
    完全二叉树子类，这些方法只对完全二叉树适用.
    '''
    def showTree(self):
        '''
        将一个列表以常见的树形结构打印出完全二叉树。存在一定误差
        :return:
        '''
        totalLen = len(self._elems)
        layerCount = 0
        flag = 0
        while totalLen > flag:
            flag += pow(2,layerCount)
            layerCount += 1

        totalWidth = pow(2,layerCount-1) * 3 - 2
        def showLine(slice,layer):
            slice = list(slice)
            length  = pow(2,layer)
            if len(slice) < length:
                slice.extend(list(' ' * (length-len(slice))))  # 用空格补齐本行到2的次方个数，防止最后一行输出错乱
            wsLen = (totalWidth - length) / (length + 1)
            for item in slice:
                sys.stdout.write(' '*wsLen)
                sys.stdout.write(str(item))
            sys.stdout.write(' '*wsLen)
            sys.stdout.write('\n')

        # for layer in range(layerCount):
        #     print self._elems[pow(2,layer)-1:pow(2,layer+1)-1]
        for layer in range(layerCount):
            showLine(self._elems[pow(2,layer)-1:pow(2,layer+1)-1],layer)

    def makeRootNode(self,lst,rootIdx=0,parentNode=None,**kwargs):
        '''
        允许递归地通过一个列表生成一个二叉树节点集群
        再通过loadTree方法将简易的二叉树对象包装成BinTree对象
        :param lst:
        :param rootIdx:
        :return:
        '''
        if rootIdx >= len(lst):
            return None
        rootNode = BinTNode(lst[rootIdx])
        rootNode.parent = parentNode
        rootNode.type = kwargs.get('type')
        rootNode.left = self.makeRootNode(lst,rootIdx*2+1,rootNode,type='l')
        rootNode.right = self.makeRootNode(lst,rootIdx*2+2,rootNode,type='r')
                            # left=self.makeRootNode(lst,rootIdx*2+1,),
                            # right=self.makeRootNode(lst,rootIdx*2+2)
        return rootNode

    def loadTree(self,lst):
        self._elems = list(lst)
        if len(self._elems) > 0:
            self.setRootNode(
                    self.makeRootNode(self._elems))

if __name__ == '__main__':
    tree = FullBinTree()
    tree.loadTree([1,2,5,7,8])
    tree.showTree()
    for i in tree.preorderIter():
        print i.data,