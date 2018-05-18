class NotSolved(Exception):
    pass


class EquationSystem:
    def __init__(self):
        self._equation_list = []
        self._solutions = {}

    def add(self, equation):
        self._equation_list.append(equation.clon())

    def get_name_set(self):
        return self._get_equation_list_name_set(self._equation_list)

    def get_last_before(self, before):
        return self._equation_list[before - 1]

    def set_solution(self, name, equation):
        self._solutions[name] = equation

    def _get_equation_list_name_set(self, equation_list):
        name_set = set()
        for equation in equation_list:
            name_set.update(equation.get_name_set())
        return name_set

    def get_solution(self, name):
        if name not in self._solutions:
            raise NotSolved
        return self._solutions[name]

    def _simplify_equations(self):
        for eq in self._equation_list:
            eq.simplify()

    def __str__(self):
        return '\n'.join(str(equation) for equation in self._equation_list)
