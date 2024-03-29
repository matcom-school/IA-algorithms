from typing import Protocol, List, Iterable
import copy

class AssignationError(Exception):
    pass

class CspDomain:
    @property
    def root(self):
        pass

    def adj_nodes(self, node) -> List[int]:
        pass
    
    def domain_of(self, node) -> Iterable:
        pass
    
    def validate(self, node_a, value_a, node_b, value_b) -> bool:
        pass

    def assign_callback(self, value, current_domains):
        return current_domains

    def callback(self, assignation):
        pass

class SearchState:
    def __init__(self, n, n_domains, step = 0) -> None:
        self.n = n
        self.n_domains = n_domains
        self.step = step

    @property
    def assignation(self) -> List:
        return [item[0] for item in self.n_domains]

    @property
    def is_finished(self) -> bool:
        return all(map(lambda x:len(x) == 1, self.n_domains))

    def __copy__(self):
        new_domains = [None] * self.n
        
        for i in range(self.n):
            new_domains[i] = copy.copy(self.n_domains[i])

        return SearchState(self.n, new_domains, self.step + 1)    

class BacktrackingSearch:
    def __init__(self, n, domain: CspDomain) -> None:
        self.problem_domain = domain
        self.first_state = SearchState(
            n, [list(self.problem_domain.domain_of(i)) for i in range(n)], 
        )

    def __compute_new_domain_for_edge(self, a, b, state: SearchState):
        new_domain = copy.deepcopy(state.n_domains[b])
        for b_values in state.n_domains[b]:
            for a_values in state.n_domains[a]:
                if self.problem_domain.validate(a, a_values, b, b_values):
                    break
            else:
                new_domain.remove(b_values)

        return new_domain

    def __assign(self, var, value, state: SearchState) -> CspDomain:
        new_state = copy.copy(state)
        new_state.n_domains = self.problem_domain.assign_callback(value, new_state.n_domains)
        new_state.n_domains[var] = [value]
        # constraint propagation 
        # edges consistence 
        Q = [var]
        while len(Q) != 0:
            v = Q.pop(0)
            for adj_node in self.problem_domain.adj_nodes(v):
                domain = new_state.n_domains[adj_node]
                new_domain = self.__compute_new_domain_for_edge(v, adj_node, new_state)
                if len(new_domain) == 0: 
                    raise AssignationError
                if len(domain) != len(new_domain):
                    new_state.n_domains[adj_node] = new_domain
                    if not adj_node in Q: Q.append(adj_node)

        return new_state
    
    def __select_var_to_assign(self, problem_state: SearchState):
        pivot, index = float('inf'), None
        for i, domains in enumerate(problem_state.n_domains):
            if len(domains) < pivot and len(domains) != 1:
                pivot, index = len(domains), i
        if index is None:
            assert not index is None
        return index 
    
    def __sorted_values(self, var, problem_state: SearchState):
        saved_domain = problem_state.n_domains[var]
        pd = [None] * len(saved_domain)
        
        for i, value in enumerate(saved_domain):
            problem_state.n_domains[var] = [value]
            s = 0
            for adj_node in self.problem_domain.adj_nodes(var):
                nd = self.__compute_new_domain_for_edge(var, adj_node, problem_state)
                s += len(problem_state.n_domains[adj_node]) - len(nd)
            
            pd[i] = (value, s)
        
        problem_state.n_domains[var] = saved_domain
        pd.sort(key=lambda x: x[1])
        for value, _ in pd:
            yield value

    def find(self):
        try:
            root = self.problem_domain.root
        except AttributeError:
            root = self.__select_var_to_assign(self.problem_domain)
        
        for value in self.first_state.n_domains[root]:
            try:
                self.__find(self.__assign(root, value, self.first_state))
            except AssignationError:
                pass

    def __find(self, problem_state):
        if problem_state.is_finished:
            return self.problem_domain.callback(problem_state.assignation)

        var = self.__select_var_to_assign(problem_state)
        for value in self.__sorted_values(var, problem_state):
            try:
                next_state = self.__assign(var, value, problem_state)
                self.__find(next_state)
            except AssignationError:
                pass

