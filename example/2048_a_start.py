def objectiveFunc(game):
    return game[1].is_game_finished()

def adjFunc(game):
    if game[1].is_game_finished():
        return []
    
    for move in "nsew":
        new_game = game[1].play(move)

        if (new_game != game[1]):
            yield (game[0] + 1, new_game)

def heuristicFunc(game):
    return max(0, 2048 - sum(sum(game[1].board, []))/2)

if __name__ == '__main__':
    from search import AStart
    from problems.game_2048 import Game
    import time

    game = Game(4, 2048)
    search_algorithm = AStart()
    start = time.time()
    length, _ = search_algorithm.find((0, game), objectiveFunc, adjFunc)

    print('spent time:', time.time() - start)
    print('length of path:', length)
    print('explored instaces:', search_algorithm.expanded)
