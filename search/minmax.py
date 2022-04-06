from multiprocessing.dummy import Array
from tools.tools import oo
from data_struct.heap import PythonHeap

class MinMax:
    def __init__(self, depth, branching_factor_percentage = 1) -> None:
        self.depth = depth
        self.bfp = branching_factor_percentage

    def create_heap(self, node, player, factor = 1):
        heap = PythonHeap()
        adjList = [ adj for adj in self.__adjFunc(node, player)]

        for _ in range(int(len(adjList) * self.bfp)):
            action = adjList[0]
            adjList.remove(action)
            adj_node, next_player = self.__transicionFun(node, player, action)
            heap.append(factor * self.__heuristicFun(adj_node), (adj_node, action ,next_player))
        
        for action in adjList:
            adj_node, next_player = self.__transicionFun(node, player, action)
            heap.append(oo, (adj_node, action ,next_player))

        return heap

    def max(self, node, player, objectiveFunc, adjFunc, transactionFunc, heuristicFun= lambda x: 0):
        self.__heuristicFun = heuristicFun
        self.__transicionFun = transactionFunc
        self.__objectiveFunc = objectiveFunc
        self.__adjFunc = adjFunc
        self.__objectiveValue = oo
        value, action = self.__max__(node, None, player, self.depth)
        return action

    def __max__(self, node, play, player, depth, alpha = -oo, beta = oo):
        if self.__objectiveFunc(node):
            return (self.__objectiveValue, play)

        heap = self.create_heap(node, player, -1)
        best = -oo
        best_action = None
        while not heap.empty:
            h_value, (adj_node, action, next_player) = heap.pop()
            if depth == 1: 
                return (h_value, action)
            best_min, action_min = self.__min__(adj_node, action, next_player, depth-1, alpha, beta)

            if best_min > best or best < best_min:
                best, best_action = best_min, action_min
            
            if best >= beta: break
            if best < beta: beta = best

        return (best, best_action)

    def min(self, node, player, objectiveFunc, adjFunc, transactionFunc, heuristicFun= lambda x: 0):
        self.__heuristicFun = heuristicFun
        self.__transicionFun = transactionFunc
        self.__objectiveFunc = objectiveFunc
        self.__adjFunc = adjFunc
        self.__objectiveValue = -oo
        value, action = self.__min__(node, None, player)
        return action
        
    def __min__(self, node, play, player, depth ,alpha = -oo, beta = oo):
        if self.__objectiveFunc(node):
            return (self.__objectiveValue, play)

        heap = self.create_heap(node, player)
        
        best = oo
        best_action = None
        while not heap.empty:
            h_value, (adj_node, action, next_player) = heap.pop()
            if depth == 1: 
                return (h_value, action)
            best_max, action_max = self.__max__(adj_node, action, next_player, depth-1, alpha, beta)

            if best_max < best or best > best_max:
                best, best_action = best_max, action_max

            if best <= alpha: break
            if best > alpha: alpha = best
        
        return (best, best_action)

        