from copy import deepcopy


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

    def get_equation_list(self):
        return self._equation_list

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

    def simplify(self):
        for eq in self._equation_list:
            eq.simplify()

    def move_variable_to_side(self, variable_name, side):
        for eq in self._equation_list:
            eq.move_variable_to_side(variable_name, side)

    def move_constant_to_side(self, side):
        for eq in self._equation_list:
            eq.move_constant_to_side(side)

    def get_equation_with_name(self, name):
        for eq in self._equation_list:
            if name in eq.get_name_set():
                return eq

    def pop_solution_equations(self):
        solution_equations = {}
        temporal_equations = []
        for eq in self._equation_list:
            if eq.is_solution_equation():
                solution_equations[eq.get_name_set().pop()] = eq
            else:
                temporal_equations.append(eq)
        self._equation_list = temporal_equations
        return solution_equations

    def clon(self):
        return deepcopy(self)

    def __str__(self):
        return '\n'.join(str(equation) for equation in self._equation_list)
