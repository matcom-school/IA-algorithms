def minimal_sub_sets(set_list):
    result = []
    set_list = [set(l) for l in set_list]
    
    while any(set_list):
        s = set_list.pop(0)

        for i, ss in enumerate(set_list):
            temp = s.intersection(ss)
            if any(temp): continue
            s = temp
            set_list.pop(i)
        
        result.append(list(s))
    
    return result
