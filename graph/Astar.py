# Implements Astar
# By: Vishnu Devarakonda
from graph import Graph
from search import Search
from heapq import heappop, heappush

class Astar(Search):
    def __init__(self, graph : Graph, heuristic) -> None:
        super().__init__(graph)
        self._h = heuristic

    def run(self, source: int, target : int):
        mH = [(0, source, (None, None))]
        seen = set([source])
        actions = []
        path = {source: (None, None)}
        while mH:
            _, node, par  = heappop(mH)
            if node == target:
                parent, act = par
                actions.insert(0, act)
                while parent:
                    parent, act = path[parent]
                    if act != None:
                        actions.insert(0, act)
                break
            neighbors = self._graph.G[node]
            for n, a in neighbors:
                if n not in seen:
                    path[n] = (node, a)
                    heappush(mH, (self._h(n), n, (node, a)))
                    seen.add(n)
        return actions