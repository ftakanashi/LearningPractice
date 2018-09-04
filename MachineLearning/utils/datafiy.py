# -*- coding:utf-8 -*-

from numpy import array

def main():

    with open('melonSet3.0','r') as dataFile:
        content = dataFile.readlines()

    res = []
    knowledege = [{} for i in range(len(content[0].split(',')))]
    for line in content:
        tmp = []
        fields = line.split(',')
        for i,field in enumerate(fields):
            if i == 0: continue
            try:
                value = float(field)
            except ValueError,e:
                if field not in knowledege[i]:
                    if len(knowledege[i]) > 0:
                        knowledege[i][field] = max(knowledege[i].values()) + 1
                    else:
                        knowledege[i][field] = 0
                value = knowledege[i][field]
            finally:
                tmp.append(value)

        res.append(tmp)

    return array(res),knowledege

if __name__ == '__main__':
    res,know = main()
    print list(res[:,:-1])
    for d in know:
        print d


