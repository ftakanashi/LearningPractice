# -*- coding:utf-8 -*-
from Heap import HeapQueue
from BinTree import BinTree,BinTNode

class WeightTNode(BinTNode):
    def __lt__(self, other):
        return self.data[1] < other.data[1]

def huffman(_dataSet):
    dataSet = [WeightTNode((item[0],item[1])) for item in _dataSet]
    heap = HeapQueue(dataSet)
    while len(heap) > 1:
        t1,t2 = heap.dequeue(),heap.dequeue()
        newNode = BinTNode(('',t1.data[1]+t2.data[1]),t1,t2)
        t1.parent = newNode
        t2.parent = newNode
        t1.type = 'l'
        t2.type = 'r'
        heap.enqueue(newNode)

    return BinTree(heap.dequeue())

if __name__ == '__main__':
    ofteness = {'a':12,'b':2,'c':5,'d':10,'e':11,'f':4,'g':3,'h':7}
    tree = huffman([(k,v) for k,v in ofteness.iteritems()])
    code_map = {}
    for node in tree.preorderIter():
        tmp = []
        if node.left is None and node.right is None:  # 到达叶子节点
            char = node.data[0]
            while node.parent is not None:
                if node.type == 'l':
                    tmp.append('0')
                elif node.type == 'r':
                    tmp.append('1')
                else:
                    raise Exception('!')
                node = node.parent
            code_map[char] = ''.join(reversed(tmp))

    print code_map





