import heapq

class Item:
    def __init__(self,t):
        self.t=t
        self.priority=t[0]
        self.item=t[1]

    def __getitem__(self,index):
        return self.t.__getitem__(index)

    def __lt__(self,other):
       return self.priority < other.priority

class PythonHeap:
    def __init__(self) -> None:
        self.heap = []
        self.func = lambda x : x

    @property
    def empty(self):
        return not any(self.heap)

    def append (self, priority, value):
        return heapq.heappush(self.heap, Item((priority, value)))

    def pop(self):
        return heapq.heappop(self.heap)
    
    def set_cmp_func(self, func):
        self.func = func