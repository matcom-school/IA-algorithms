class Var:
    def __init__(self) -> None:
        self.value = None
        self.is_assing = False
    
    def assing(self, value):
        self.is_assing = True
        self.value = value
    
    def get_value(self):
        if not self.is_assing: raise ValueError()
        return self.value

    def unassign(self):
        self.is_assing = False

class BacktrackingSearch:
    def __set_domain_restrition(self, domains, binary_restriction, global_restrition):
        self.domains = domains
        self.binary_restriction = binary_restriction
        self.global_restriction = global_restrition

    def find_solution(self, domains, binary_restriction, global_restrition):
        self.__set_domain_restrition(domains, binary_restriction, global_restrition)
        return self.__back_tracking_search([Var() for _ in domains])
    
    def _connected_component():
        pass

    def _cut_set():
        pass

    def __back_tracking_search(self, vars):
        is_completed, result = self.is_complete_and_solution(vars)
        if is_completed: return result

        index = self._select_unassign_var(vars)
        for value in self._order_domain_consisten_value(index, vars):
            vars[index].assign(value)
            result = self.__back_tracking_search(vars)
            if not result is None: return result
            vars[index].unassign()
        
        return None

    def _consisten_edge(index, vars):
        pass

    def _select_unassign_var(self, vars):
        index = None
        domain_len = None
        for i, var in vars:
            if not var.is_assing:
                if i is None: index, domain_len = i, len(self.domains[i])
                temp = len(self.domains[i])
                if temp < domain_len: index, domain_len = i, temp

        return index
    
    # menor valor de consisten_edge
    def _order_domain_consisten_value(self, index, vars):
        pass

    def is_complete_and_solution(self, vars):
        result = []
        for var in vars:
            try: result.append(var.get_value())
            except ValueError: return False, None
        
        for f in self.global_restriction:
            if not f(result): return True, None
        
        return True, result
    