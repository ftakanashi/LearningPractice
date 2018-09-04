# -*- coding:utf-8 -*-

class HashMapException(Exception):
    pass

class HashMap:
    '''
    哈希表实现，将字符串键和任意类型的值保存起来
    冲突消解办法是内消解（开地址），探查序列生成方式为双散列探查
    '''
    def __init__(self,length):
        self.length = length
        self._elems = [None] * length

    def _str2num(self,s,base=29):
        res = 0
        for ch in s:
            res = res * base + ord(ch)
        return res

    def _searchSeq(self,i):
        '''
        双散列中的第二个散列函数
        要求其返回值与表长互素（当然，默认表长作为第一个散列函数的除余法基数时）
        :param i:
        :return:
        '''
        res = i % 7  # 7是任选的数字，一般要求这个数字要小于表长
        while res == 0 or res * (self.length // res) == self.length:
            res += 1
        return res

    def _locate(self,key):
        '''
        寻址方法，根据传递进来的键返回出一个具体的下标（如果有候选的话）
        :param key:
        :return:
        '''
        n_key = self._str2num(key)  # 基数转换
        possible_index = n_key % self.length  # 除余法获得第一候选
        crash_count = 0  # 记录冲突次数，也可以作为判断表满的flag
        step = self._searchSeq(n_key)  # 二次散列的步长，与表长互素
        base = possible_index  # 二次散列的基数。注意这个base也是不变的，并不随possible_index的变化而变化
        while self._elems[possible_index] is not None and self._elems[possible_index][2] and key != self._elems[possible_index][0]:
            # 循环的各个条件：1. 若找到某个下标的值还是None，未发生冲突 2. 某个下标被标记为已删除，可以被替换值了 3. 找到下标中记录的key就是想要定位的key
            # 满足任意一个条件，便可跳出循环，返回这个下标做相关处理
            possible_index = (base + crash_count * step) % self.length  #由于step和表长互素，可以证明这一步，如果需要可以遍历到表中每个下标
            crash_count += 1
            if crash_count == self.length:  # 已经遍历完所有下标（冲突了表长-1次）仍未找到合适的下标值。表名表满了
                return None
        return possible_index

    def set(self,key,value):
        i = self._locate(key)
        if i is not None:
            self._elems[i] = [key,value,True]  # 第三个值是删除标记，当打成False意味着此位置的k-v对逻辑上应已经删除，不置为None是为了防止它在某些其他元素搜索路径上，那些元素会找不到
        else:
            raise HashMapException('Full Hash Map')

    def get(self,key):
        i = self._locate(key)
        if i is None or self._elems[i] is None:
            return None
        elif self._elems[i][2]:  # 只有未被打删除标签的，逻辑上还存在的值才能被get出来
            return self._elems[i][1]

    def delete(self,key):
        i = self._locate(key)
        if i is not None and self._elems[i] is not None:
            self._elems[i][2] = False  # 删除不是真的删除，只是打了删除标签

    def __str__(self):
        res = '{'
        for elem in self._elems:
            if elem and elem[2]:
                res += '%s: %s,' % (elem[0],elem[1])
        res += ' }'
        return res

    def __repr__(self):
        res = ''
        for elem in self._elems:
            res += str(elem)
            res += ', '
        return res


if __name__ == '__main__':
    hmap = HashMap(30)
    num = 0
    src = 'Four score and seven years ago, our fathers brought forth on this continent a new nation. conceived in liberty and dedicated to the proposition that all man are created equal'.split()
    for ch in src:
        hmap.set(ch,num)
        num += 1
    # print hmap.get('continent')
    # print hmap.get('and')
    print hmap.get('our')
    print hmap._locate('our')
    hmap.delete('our')
    print hmap.get('our')
    hmap.set('Frank','good')
    print hmap._locate('Frank')