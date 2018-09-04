# -*- coding:utf-8 -*-

'''
专门开一个文件来记录一下递归/非递归，DFS,BFS的各种遍历二叉树的算法
'''

class BinTree:
    '''
    说明使用的树结构
    '''
    def __init__(self,data,left=None,right=None):
        self.data = data
        self.left = left
        self.right = right

def dfs_pre_rec(tree,proc):
    '''
    递归先根序遍历
    :param tree:
    :param proc:
    :return:
    '''
    node = tree
    proc(node.data)
    if node.left is not None:
        dfs_pre_rec(node.left,proc)
    if node.right is not None:
        dfs_pre_rec(node.right,proc)

def dfs_mid_rec(tree,proc):
    '''
    递归中根序遍历
    :param tree:
    :param proc:
    :return:
    '''
    node = tree
    if node.left is not None:
        dfs_mid_rec(node.left,proc)
    proc(node.data)
    if node.right is not None:
        dfs_mid_rec(node.right,proc)

def dfs_post_rec(tree,proc):
    '''
    递归后根序遍历
    :param tree:
    :param proc:
    :return:
    '''
    node = tree
    if node.left is not None:
        dfs_post_rec(node.left,proc)
    if node.right is not None:
        dfs_post_rec(node.right,proc)
    proc(node.data)

from Queue import Queue,LifoQueue

def bfs(tree,proc):
    queue = Queue()
    node = tree
    queue.put(node)
    while not queue.empty():
        node = queue.get()
        proc(node.data)
        if node.left is not None:
            queue.put(node.left)
        if node.right is not None:
            queue.put(node.right)

def dfs_pre_nonrec(tree,proc):
    '''
    非递归前根序遍历
    :param tree:
    :param proc:
    :return:
    '''
    stack = LifoQueue()
    node = tree
    stack.put(node)
    while not stack.empty():
        node = stack.get()
        proc(node.data)
        if node.right is not None:
            stack.put(node.right)
        if node.left is not None:
            stack.put(node.left)

'''以上所有算法都还算简单的，接下来两个就稍微需要绕一绕了
'''

def dfs_mid_nonrec(tree,proc):
    '''
    非递归中根序遍历
    :param tree:
    :param proc:
    :return:
    '''
    stack = LifoQueue()
    node = tree
    while node is not None or not stack.empty():
        while node is not None:  # 遍历到最左叶节点，路径上所有左边叶节点都入栈
            stack.put(node)
            node = node.left

        node = stack.get()    # 出栈处理了数据
        proc(node.data)
        if node.right is None:    # 若当前节点没有右子节点，那么当前节点及其子树处理完毕。
            # 注意这里不可另node = stack.get(),这样的话上面的小循环node又要去处理左子树，重复处理。一定要置None
            node = None
        else:
            node = node.right  # 有右子节点的情况，就只要“递归”地再处理这个右子树即可。
            # 注意不要将右子树入栈，所有入栈操作应该都在上面那个小循环中进行

        '''
        上述对右子树存在与否的判断代码也可以简单地写成node = node.right即可
        '''

def dfs_post_nonrec(tree,proc):
    '''
    非递归后根序遍历
    :param tree:
    :param proc:
    :return:
    '''
    stack = LifoQueue()
    node = tree
    while node is not None or not stack.empty():
        while node is not None:    # 注意，这一波遍历的规则是能左则左，若不能左往右也行
            stack.put(node)
            if node.left is not None:
                node = node.left
            else:
                node = node.right

        node = stack.get()    # 这个算法的特征之一，处理某个节点的时候，栈中保存着的是这个节点的所有前辈节点
        proc(node.data)

        #### 从这里开始和中根序遍历不一样 ####
        if stack.empty():    # 若栈空，说明当前节点没有任何前辈节点，即根节点。根节点处理完成后直接跳出程序
            break

        tmp = stack.get()    # 由LifoQueue实现的栈没有peek或者top方法，自己模拟一下…
        stack.put(tmp)

        if node is tmp.left:    # 判断刚才处理的是左子节点还是右子节点
            node = tmp.right    # 左子节点的话说明右子节点还没处理
        else:
            node = None    # 右子节点的话说明tmp节点对应子树已经处理完了


if __name__ == '__main__':

    t = BinTree(0,
                BinTree(1,
                        BinTree(3),
                        BinTree(4)),
                BinTree(2,
                        BinTree(5),
                        BinTree(6)))

    def p(data):
        print data,

    dfs_pre_rec(t,p)
    print ''
    dfs_mid_rec(t,p)
    print ''
    dfs_post_rec(t,p)
    print ''
    bfs(t,p)
    print ''
    dfs_pre_nonrec(t,p)
    print ''
    dfs_mid_nonrec(t,p)
    print ''
    dfs_post_nonrec(t,p)
