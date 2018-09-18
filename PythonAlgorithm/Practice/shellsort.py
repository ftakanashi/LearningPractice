# -*- coding:utf-8 -*-

def shell_sort(lst):
    gap = len(lst) // 2
    while gap > 0:
        i = gap
        while i < len(lst):
            j = i
            while j >= gap:
                if lst[j] < lst[j-gap]:
                    lst[j-gap],lst[j] = lst[j],lst[j-gap]
                j -= gap
            i += 1
        gap /= 2

if __name__ == '__main__':
    import random
    lst = range(10)
    random.shuffle(lst)
    print lst

    shell_sort(lst)
    print lst