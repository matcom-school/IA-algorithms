import imp
from search.search_basic import SearchBasic
from data_struct.linked_list import LinkedListFIFO, LinkedListLIFO
from data_struct.heap import PythonHeap

class DFS(SearchBasic): 
    def __init__(self) -> None:
        super().__init__(LinkedListLIFO())

class BFS(SearchBasic):
    def __init__(self) -> None:
        super().__init__(LinkedListFIFO)

class Dijkstra(SearchBasic):
    def __init__(self, weightFun) -> None:
        super().__init__(PythonHeap(), weightFun)

class AStart(SearchBasic):
    def __init__(self, weightFun, heuristicFunc) -> None:
        super().__init__(PythonHeap(), weightFun, heuristicFunc)