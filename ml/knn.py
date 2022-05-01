import math
from unittest import result
from .supervised import SuperVised

def d(x, y):
    return math.sqrt(sum([xi-yi for xi, yi in zip(x, y)]))

class KNN(SuperVised):
    def __init__(self, k, distance_f = d) -> None:
        self.k = k
        self.memory = []
        self.distance = distance_f

    def training(self, X, Y):
        for x, y in zip(X, Y):
            self.memory.append((x, y))

    def predict(self, x):
        result = []
        for point, value in self.memory:
            d = self.distance(x, point)
            result.append((d, value))

            if len(result) < self.k: continue

            result.sort(key=lambda x: x[0])
            result.pop()
        
        group = {}
        for d, value in result:
            try: 
                group[value] += 1
            except KeyError:
                group[value] = 1
        
        pivot  = 0
        result = None
        for key in group.keys():
            if group[key] > pivot:
                pivot = group[key]
                result = key
        
        return result

            