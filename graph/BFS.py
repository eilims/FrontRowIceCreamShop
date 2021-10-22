#Implements BFS
#By: Zion Gutierrez
from graph import Graph
from search import Search

class BFS(Search):
    def __init__(self, graph: Graph) -> None:
        super().__init__(graph)
        
    def run(self, source : int,  target : int):
        queue = []
        parent = {}
        path = []

        for vertex in self._graph.G:
            parent[vertex] = None
        parent[source] = source
        queue.append(source)

        while queue:
            node = queue.pop(0)
            neighbors = self._graph.G[node]
            for neighbor in neighbors:
                state = neighbor[0]
                if parent[state] == None:
                    parent[state] = node
                    queue.append(state)
                if state == target:
                    break

        parentIterator = target
        while (parentIterator != source):
            path.append(parentIterator)
            parentIterator = parent[parentIterator]
        path.append(source)
        path.reverse()
        return path
