#!/usr/bin/env python3
from Agent import * # See the Agent.py file
from pysat.solvers import Glucose3

#### All your code can go here.

#### You can change the main function as you wish. Run this program to see the output. Also see Agent.py code.

kb = Glucose3()
ag = Agent()
discovered = set()
visited = set()
safe = set()
mines = set()
grid = [[0 for _ in range(4)] for _ in range(4)]
path = []
comp = 0

def convert(pos):
    """
        converts coordinates to int and vice versa
    """
    """
        1,4 2,4 3,4 4,4    13 14 15 16
        1,3 2,3 3,3 4,3    9 10 11 12
        1,2 2,2 3,2 4,2    5  6  7  8
        1,1 2,1 3,1 4,1    1  2  3  4
    """
    if type(pos) is int:
        return ((pos - 1) % 4, (pos - 1) // 4)
    return 4 * pos[1] + 1 + pos[0] % 4

def zeroIndex(co):
    return (co[0] - 1, co[1] - 1)

def subTup(a, b):
    return (a[0] - b[0], a[1] - b[1])

def findNeighbors(curLoc):
    """
        finds neighbors of a cell
    """

    res = []
    [x, y] = curLoc
    if x > 0: res.append((x - 1, y))
    if x < 3: res.append((x + 1, y))
    if y > 0: res.append((x, y - 1))
    if y < 3: res.append((x, y + 1))

    return res

def BFS(start: tuple, stop: tuple):
    """
        finds shortest path from start to stop
    """

    queue = []
    queue.append(start)
    parent = {}
    parent[start] = (-1, -1)

    while queue:
        cur = queue.pop(0)
        # print("BFS cur", cur)
        # print(findNeighbors(cur))

        stopFound = False

        for i in findNeighbors(cur):
            if grid[i[0]][i[1]] == 1 and i not in parent.keys():
                # print("BFS next neighbor", i)
                queue.append(i)
                parent[i] = cur

                if i == stop:
                    stopFound = True
                    break
        
        if stopFound: break

    # backtrack to make a path
    path = []
    cur = stop
    while cur != start:
        path.append(cur)
        cur = parent[cur]
    path.append(start)
    path.reverse()

    # print("BFS path", path)

    return path

def planPath(start: tuple, stop: tuple):
    """
        plans a path from the current cell to the next cell agent has to move to
    """

    # print("plan path from", start, "to", stop)

    path = BFS(start, stop)

    dir = {
        (-1, 0): 'Left',
        (1, 0): 'Right',
        (0, -1): 'Down',
        (0, 1): 'Up'
    }
    
    return [dir[subTup(path[i], path[i - 1])] for i in range(1, len(path))]

def moveAgent():
    """
        moves the agent to the safe cell nearest to [4,4] and updates the path
    """

    # plan the path
    moves = planPath(zeroIndex(ag.FindCurrentLocation()), convert(max(safe)))
    # print("plan", moves)

    # move agent according to the plan
    for i in moves:
        ag.TakeAction(i)
        path.append(ag.FindCurrentLocation())

    # print()

def addClauses(neighbors):
    """
        add clauses to the knowledge base corresponding to the percept given by agent
    """
    global comp
    comp+= 1

    percept = ag.PerceiveCurrentLocation()
    # print("percept", percept)

    if percept == '=0':
        for i in neighbors:
            kb.add_clause([-i])
    elif percept == '=1':
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                kb.add_clause([-neighbors[i], -neighbors[j]])
        kb.add_clause([i for i in neighbors])
    else:
        for i in neighbors:
            kb.add_clause([j for j in neighbors if i != j])

def filterCells():
    """
        solves knowledge base for every cell in discovered set and checks if they are safe to visit or they have a mine
    """

    # print("mines", mines)

    if len(mines) == 5:
        # print("mines maxed")
        for i in discovered:
            if i not in mines:
                safe.add(i)
                (x, y) = convert(i)
                grid[x][y] = 1
        discovered.clear()
        return

    remEle = []
    for i in discovered:
        if not kb.solve(assumptions=[i]):
            # definitely safe
            safe.add(i)
            remEle.append(i)
            (x, y) = convert(i)
            grid[x][y] = 1
        elif not kb.solve(assumptions=[-i]):
            # print(i, "mine found")
            # definitely has a mine
            remEle.append(i)
            mines.add(i)

    for i in remEle:
        discovered.remove(i)

    # rot90()

def updateInfo():
    """
        updates safe, visited and discovered sets and adds clauses to knowledge base
    """

    cur = convert(zeroIndex(ag.FindCurrentLocation()))
    visited.add(cur)
    safe.remove(cur)
    neighbors = [convert(i) for i in findNeighbors(zeroIndex(ag.FindCurrentLocation()))]
    # print("neigbors", neighbors)

    for i in neighbors:
        if i not in visited and i not in safe:
            discovered.add(i)

    addClauses(neighbors)
    filterCells()

def initialize():
    """
        add some initial info to kb, safe, visited, discovered, path and grid
    """

    kb.add_clause(range(1,17))
    kb.add_clause([-1])
    kb.add_clause([-16])
    kb.add_clause([-17])

    safe.add(1)

    visited.add(17)

    grid[0][0] = 1
    grid[3][3] = 1

    path.append([1, 1])


def rot90():
    for i in range(4):
        for j in range(4):
            print(grid[j][3-i], end=" ")
        print()

def finalMove():
    if convert(zeroIndex(ag.FindCurrentLocation())) == 15:
        ag.TakeAction('Right')
    else:
        ag.TakeAction('Up')

    path.append(ag.FindCurrentLocation())





def play():

    initialize()
    
    while convert(zeroIndex(ag.FindCurrentLocation())) != 16:
        # print("Current Location", ag.FindCurrentLocation(), convert(zeroIndex(ag.FindCurrentLocation())))
        updateInfo()
        if not safe:
            print("Heavy Case")
            break
        # print("safe {}".format(safe), "discovered {}".format(discovered), "visited {}".format(visited), sep="\n")
        moveAgent()

    print("\nPath taken by agent:", " > ".join(["[{}, {}]".format(i[0], i[1]) for i in path]), sep="\n")
    # print("Path len =", len(path))
    # for i in path:
    #     print(i, end=" => ")
    # print()
    # rot90()

if __name__ == "__main__":
    play()