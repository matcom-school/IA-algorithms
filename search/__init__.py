import imp
from .search_basic import SearchBasic
from ..data_struct.linked_list import LinkedListFIFO, LinkedListLIFO
from ..data_struct.heap import PythonHeap

class DFS(SearchBasic): 
    def __init__(self) -> None:
        super().__init__(LinkedListLIFO())

class BFS(SearchBasic):
    def __init__(self) -> None:
        super().__init__(LinkedListFIFO)

class Dijkstra(SearchBasic):
    def __init__(self, weightFun = None) -> None:
        super().__init__(PythonHeap(), weightFun)

class AStart(SearchBasic):
    def __init__(self, weightFun = None, heuristicFunc = None) -> None:
        heap = PythonHeap()
        heap.func = lambda x : x.weight
        super().__init__(heap, weightFun, heuristicFunc)