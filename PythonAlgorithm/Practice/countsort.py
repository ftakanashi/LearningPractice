# -*- coding:utf-8 -*-

def generate(n):
    res = []
    def backtrace(s,left,right):
        if len(s) == 2 * n:
            res.append(s)
            return
        if left < n:
            backtrace(s+'(', left+1, right)
        if right < left:
            backtrace(s+')', left, right+1)
    backtrace('',0,0)
    return res

if __name__ == '__main__':
    print generate(2)