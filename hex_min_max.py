from problems.hex.game_logic import EMPTY, WHITE, BLACK
import itertools


def adj_func(game, player): 
    for i in range(game.size):
        for j in range(game.size):
            if game[i, j] == EMPTY: yield i, j

def density_result(fn):
    def f(player):
        def ff(game):
            w, b = fn(game)
            return w/b if b != 0 else w if player == WHITE else b/w if w != 0 else b
        return ff
    return f

def union(*list):
    def f(player):
        func = [f(player) for f in list]
        def play(game):
            return sum([f(game) for f in func])
        return play
    return f 

def wf(value):
    def f(func):
        def ff(player):
            _func = func(player)
            def fff(game):
                return value * _func(game)
            return fff
        return ff
    return f


@density_result
def border_heuristic(game):
    w, b, factor = 0, 0, game.size/4
    for i in range(game.size):
        for j in range(game.size):
            if factor > i or i > game.size - 1 - factor:
                w += 1 if game[i, j] == WHITE else 0
            if factor > j or j > game.size - 1 - factor:
                b += 1 if game[i, j] == BLACK else 0
    return w, b

@density_result
def lineal_heuristic(game):
    if game.size < 3: return 0
    w, b, = [0] * game.size, [0] * game.size,
    for i in range(game.size):
        for j in range(game.size):
            w[i] += 1 if game[i,j] == WHITE else 0
            b[j] += 1 if game[j,i] == WHITE else 0
    
    w_pivot = w[0] + w[1] + w[2]
    b_pivot = b[0] + b[1] + b[2]
    index = 0
    for i in range(3, game.size):
        if w_pivot < w_pivot - w[index] + w[i]:
            w_pivot = w_pivot - w[index] + w[i]
        
        if b_pivot < b_pivot - b[index] + b[i]:
            b_pivot = b_pivot - b[index] + b[i]        
        
        index += 1
    
    return w_pivot, b_pivot

@density_result
def dynamic_heuristic(game):
    cost_w = [[0] * game.size for _ in range(game.size)]
    cost_b = [[0] * game.size for _ in range(game.size)]

    def check(i, j):
        return i >= 0 and i < game.size and j >= 0 and j < game.size
    
    def weight_func(player):
        def f(i, j):
            if player == game[i,j]: return 1
            elif EMPTY == game[i,j]: return 0.5
            else: return -0.5
        return f

    def filter(*pos):
        for i, j in pos:
            if check(i,j): 
                yield (i, j)

    w_w = weight_func(WHITE)
    for j in range(game.size):
        for i in range(game.size):
            cost_w[i][j] = (
                w_w(i, j) + 
                max([cost_w[x][y] for x, y in filter((i-1, j-1), (i, j-1), (i + 1, j-1))] + [0])
            )
    
    w_b = weight_func(WHITE)
    for i in range(game.size):
        for j in range(game.size):
            cost_b[i][j] = (
                w_b(i, j) + 
                max([cost_b[x][y] for x, y in filter((i - 1, j - 1), (i - 1, j), (i - 1, j + 1))] + [0])
            )


    return max(cost_w[i][game.size -1] for i in range(game.size)), max(cost_b[game.size - 1])

def change_player(player):
    if player == WHITE: return BLACK
    return WHITE

def def_play(h, depth = 3, percentage = 3/10):
    minmax = MinMax(depth, percentage)
    def play(game, player):
        return minmax.max(game, player, 
     objectiveFunc=lambda game: game.winner() != EMPTY,
     adjFunc= adj_func,
     transactionFunc= lambda game, player, action: (game.clone_play(action[0], action[1]), change_player(player)),
     heuristicFun=h(player)
     )
    return play

def auto_min_max(depth, percentage, function, values):
    player = []
    for d in depth:
        for p in percentage:
            for s in itertools.product(values, repeat=len(function)):
                name = f"({d})depth_({p})branch_precentage_"
                f = []
                for i, v in enumerate(s):
                    
                    name += f'({v}){function[i]}_'
                    f.append((v, function[i]))
                player.append((d, p, name, f))
    return player

def sampling(x_len, value, _sampling):
    if x_len == len(_sampling):
        return [[i for  i in _sampling]]
    
    _sampling.append(None)
    result = []
    for v in value:
        _sampling[-1] = v
        result += sampling(x_len, value, _sampling)
    
    return result

if __name__ == '__main__':
    from problems.hex.tourney import tourney
    from problems.hex.game_logic import EMPTY, WHITE, BLACK
    from search.minmax import MinMax
    import time

    BORDER = "border"
    LINEAL = "lineal"
    DIJKSTRA = 'dijkstra'
    a = auto_min_max([3,4,5], [ i/10 for i in range(3, 7) ], [BORDER, LINEAL, DIJKSTRA], [0, 0.1, 0.3, 0.5, 0.8, 1])

    player = []
    func_dict = {
        BORDER: border_heuristic,
        LINEAL: lineal_heuristic,
        DIJKSTRA: dynamic_heuristic
    }
    for d, p, name, f in a:
        values = [v for v, _ in f]
        if 0 in values:
            values.remove(0)
            if sum(values) == max(values) != 1: continue 
        player.append( (name, def_play(union(*tuple([wf(value)(func_dict[func]) for value, func in f])), d, p)) )
    start = time.time()
	
    tourney(player)
    
    print('spent time:', time.time() - start)


# Ranking:
# minmax_border_lineal_0.3 45
# minmax_border_lineal 45
# minmax_border 45
# minmax_border_dijkstra_0.3 42
# minmax_border_dijkstra 37
# problems.hex.random_player 23
# minmax_lineal 22
# minmax_dijkstra 16
# problems.hex.rush_player 13

# spent time: 6726.333554983139