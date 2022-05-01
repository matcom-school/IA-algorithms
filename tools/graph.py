def cycle_list(adj_list): 
    _len = len(adj_list)
    paths = [None for _ in range(_len + 1)]
    cycles_edge = []
    visited = []

    def dfs(v, father):
        visited.append(v)
        paths[v] = paths[father] + [v]

        for w in adj_list[v]:
            if w in visited: cycles_edge.append((v, w))
            else: dfs(w, v)

    paths[_len] = []
    dfs(0, _len)

    result = []
    for v, w in cycles_edge:
        eq_path_len = len(list(zip(paths[v], paths[w])))
        result.append(paths[v][eq_path_len-1:] + paths[w][eq_path_len-1:])
    
    return result