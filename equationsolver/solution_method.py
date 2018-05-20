from equationsolver.equation import Side


class NotSolved(Exception):
    pass


class SolutionMethod:
    def __init__(self):
        self._equation_system = None
        self._solutions = {}

    def set(self, equation_system):
        self._equation_system = equation_system

    def resolve(self):
        raise NotImplemented

    def set_solution(self, name, equation):
        self._solutions[name] = equation

    def get_solution(self, name):
        if name not in self._solutions:
            raise NotSolved
        return self._solutions[name]

    def get_solutions_name_set(self):
        return set(self._solutions.keys())

    def get_solution_value(self, name):
        return self._solutions[name].get_value_constant(Side.right)
