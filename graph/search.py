# Defines the base class for search algorithm
# By: Vishnu Devarakonda
from graph import Graph

class Search:
    def __init__(self, graph: Graph) -> None:
        self._graph = graph

    def run(self, source: int, target: int):
        raise NotImplementedError