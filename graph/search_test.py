from graph import Graph
from DFS import DFS
from BFS import BFS
from Astar import Astar

g = Graph()
bfs = BFS(g)
print(bfs.run(0,1))

dfs = DFS(g)
print(dfs.run(0, 1))

def h(a):
    aX = a % 8
    aY = a // 8
    bX = 1 % 8
    bY = 1 // 8
    return ((aX-bX)**2 + (bX-bY)**2)**.5

astar = Astar(g, h)
print(astar.run(0, 1))

# [4, 5, 4, 3, 2, 3, 0, 6, 6, 7, 1, 1, 0]
# [3, 6, 1]