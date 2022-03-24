class ItemSearch:
    def __init__(self, weight, node) -> None:
        self.weight = weight
        self.node = node

class SearchBasic:
    def __init__(self, data_struct, weightFunc = None, heuristicFunc = None) -> None:
        self.data_struct = data_struct
        self.weightFunc = weightFunc if not weightFunc is None else lambda x, y: x.weight + 1
        self.heuristicFunc = heuristicFunc if not heuristicFunc is None else lambda x : 0

    def find(self, start, objectiveFunc, adjFunc): 
        self.data_struct.append(ItemSearch(0, start))

        self.expanded = 0
        while not self.data_struct.empty:
            expanded_node = self.data_struct.pop()
            self.expanded += 1

            if objectiveFunc(expanded_node): return expanded_node

            for adj in adjFunc(expanded_node):
                self.data_struct.append(ItemSearch(self.weightFunc(expanded_node, adj) + self.heuristicFunc(adj), adj))
        
        return None
