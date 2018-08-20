# -*- coding:utf-8 -*-

MAZE = [
    [1] * 14,
    [1,0,0,0,1,1,0,0,0,1,0,0,0,1],
    [1,0,1,0,0,0,0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,1,0,1,0,1,0,1],
    [1,0,0,0,1,1,1,1,0,0,0,1,0,1],
    [1] * 14
]

START = [1,1]
END = [4,12]

DIRS = [(0,1),(1,0),(0,-1),(-1,0)]

import Queue

def get(maze,pos):
    return maze[pos[0]][pos[1]]

def mark(maze,pos):
    maze[pos[0]][pos[1]] = 1

def cancel(maze,pos):
    maze[pos[0]][pos[1]] = 0

def passable(maze,pos):
    return get(maze,pos) == 0

def solve_maze_byQueue(maze,start,end):
    queue = Queue.Queue()
    curr = start
    mark(maze,curr)
    if curr == end:
        return
    queue.put({'curr':curr,'his':[]})  # 要点 记录每到达一个位置时其历史路径，方便最终给出结果
    while not queue.empty():
        curr = queue.get()
        for i in range(4):
            curr_pos = curr.get('curr')
            new_pos = [curr_pos[0] + DIRS[i][0],curr_pos[1] + DIRS[i][1]]
            if passable(maze,new_pos):
                if new_pos == end:
                    print curr.get('his') + [i]
                    return
                mark(maze,new_pos)
                his = curr.get('his') + [i]
                queue.put({'curr':new_pos,'his':his})

def solve_mazeStack(maze,start,end):
    stack = Queue.LifoQueue()
    curr = start
    if curr == end:
        return
    mark(maze,curr)
    stack.put((curr,0))    # 要点 将每个位置的已检查方向一起加入栈，方便前面路不通时回过来之后直接进行下一个方向的探索
    while not stack.empty():
        pos,dirIdx = stack.get()
        for i in range(dirIdx,4):  # 只需要往之前没有探索过的地方探索即可
            new_pos = [pos[0]+DIRS[i][0],pos[1]+DIRS[i][1]]
            if new_pos == end:
                while not stack.empty():
                    print stack.get()[1]-1,
                return
            if passable(maze,new_pos):
                stack.put((pos,i+1))
                mark(maze,new_pos)
                stack.put((new_pos,0))
                break


if __name__ == '__main__':
    solve_mazeStack(MAZE,START,END)