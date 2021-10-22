#Implements DFS
#By: Vishnu Devarakonda
from graph import Graph
from search import Search

class DFS(Search):
    def __init__(self, graph: Graph) -> None:
        super().__init__(graph)


    def run(self, source : int,  target : int):
        STK = [(source,(None, None))]
        seen = set([source])
        actions = []
        path = {source: (None, None)}
        while STK:
            node, par = STK.pop()
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
                    STK.append((n, (node, a)))
                    seen.add(n)
        return actions