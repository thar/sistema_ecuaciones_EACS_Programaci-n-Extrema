from equationsolver.equation_system_solver import EquationSystemSolver


class NotSolved(Exception):
    pass


class EquationSystem:
    def __init__(self):
        self._equation_list = []
        self._solution_method = None
        self.equation_system_solver = None
        self._solutions = {}

    def add(self, equation):
        self._equation_list.append(equation.clon())

    def set_equation_system_solver(self, equation_system_solver):
        self.equation_system_solver = equation_system_solver

    def set(self, solution_method):
        self._solution_method = solution_method
        self._solution_method.set(self)
        self.equation_system_solver = EquationSystemSolver(self, self._solution_method)

    def resolve(self):
        self.equation_system_solver.resolve()

    def get_name_set(self):
        return self._get_equation_list_name_set(self._equation_list)

    def __get(self, index):
        return self._equation_list[index]

    def get_last_before(self, before):
        return self._equation_list[before - 1]

    def get_last(self):
        return self._equation_list[-1]

    def copy_before_before(self, before):
        self._equation_list = self._equation_list[:before] + self.__get(before).clon() + self._equation_list[before:]

    def copy_before(self):
        self.add(self.get_last())

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

    def equal(self):
        return False

    def __str__(self):
        return '\n'.join(str(equation) for equation in self._equation_list)
