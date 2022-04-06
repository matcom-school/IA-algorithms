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

    def decrease_key(self, priority, value):
        for i, (p, x) in enumerate(self.heap):
            if x == value:
                if p < priority: return
                self.heap[i] = Item((priority, value))
                break
        heapq.heapify(self.heap)
    
    def set_cmp_func(self, func):
        self.func = func

class SetHeap(PythonHeap):
    def __init__(self) -> None:
        super().__init__()
        self.open_set = set()
        self.close_set = set()
    
    def append(self, priority, value):
        if value in self.close_set: return 

        if value in self.open_set:
            self.decrease_key(priority, value)
            return 

        self.open_set.add(value)
        return super().append(priority, value)
    
    def pop(self):
        p, v = super().pop()
        self.open_set.remove(v)
        self.close_set.add(v)
        return p, v
    
