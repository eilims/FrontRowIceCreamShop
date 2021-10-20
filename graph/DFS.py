import Graph from Graph

class DFS(Search):
    def __init__(self, graph: Graph) -> None:
        super().__init__(graph)


    def run(self, source : int,  target : int):
        STK = [(source,None)]
        seen = set([])
        actions = []
        while STK:
            node,a = STK.pop()
            if node == target:
                actions = [p[1] for p in STK[1:]]
                break
            if node not in seen:
                neighbors = self._graph[node]
                for n, a in neighbors:
                    STK.append(n)
                seen.add(node)
        return actions