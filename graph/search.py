# Defines the base class for search algorithm
# By: Vishnu Devarakonda
import Graph from Graph


class Search:
    def __init__(self, graph: Graph) -> None:
        self._graph = Graph

    def run(self, source: int, target: int):
        raise NotImplementedError