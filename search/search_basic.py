class SearchBasic:
    def __init__(self, data_struct, weightFunc = None, heuristicFunc = None) -> None:
        self.data_struct = data_struct
        self.weightFunc = weightFunc if not weightFunc is None else lambda x, y: 1
        self.heuristicFunc = heuristicFunc if not heuristicFunc is None else lambda x : 0

    def find(self, start, objectiveFunc, adjFunc): 
        self.data_struct.append(0, start)
        self.heuristicValue = {start: 0}
        self.parent = {start: None}

        self.expanded = 0
        while not self.data_struct.empty:
            cost, node = self.data_struct.pop()
            if objectiveFunc(node): return node

            for adj in adjFunc(node):
                self.heuristicValue[adj] = self.heuristicFunc(adj)
                cost = cost - self.heuristicValue[node] + self.weightFunc(node, adj) 
                self.data_struct.append(cost + self.heuristicValue[adj], adj)
                self.parent[adj] = (node, cost)
                self.expanded += 1
        
        return None

    def map_parent(self, node, func = lambda x, y: x.insect(0, y), default = []):
        result = default
        while not node is None:
            result = func(result, node)
            node = self.parent[node]
        
        return result