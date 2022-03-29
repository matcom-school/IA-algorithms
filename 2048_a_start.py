open_set = set()

def objectiveFunc(game):
    return game.is_game_finished()

def adjFunc(game):
    if game.is_game_finished():
        return []
    
    for move in "nsew":
        new_game = game.play(move)

        if new_game != game and not new_game in open_set:
            open_set.add(new_game)
            yield new_game

def heuristicFunc(game):
    return max(0, 2048 - sum(sum(game.board, []))/2)

if __name__ == '__main__':
    from search import AStart
    from problems.game_2048 import Game
    import time

    game = Game(4, 2048)
    search_algorithm = AStart(heuristicFunc=heuristicFunc)
    start = time.time()
    node = search_algorithm.find(game, objectiveFunc, adjFunc)

    print('spent time:', time.time() - start)
    print('length of path:', search_algorithm.map_parent(node, func = lambda x,y: x + 1, default= 0))
    print('explored instaces:', search_algorithm.expanded)
