from copy import deepcopy

from equationsolver.equation import Side, Equation


class EquationSystem:
    def __init__(self):
        self._equation_list = []

    def add(self, equation):
        self._equation_list.append(equation.clon())

    def remove(self, equation):
        if equation in self._equation_list:
            self._equation_list.remove(equation)

    def get_name_set(self):
        name_set = set()
        for equation in self._equation_list:
            name_set.update(equation.get_name_set())
        return name_set

    def apply_operation(self, operation):
        operation(self._equation_list)

    def get_equation_with_name(self, name):
        for eq in self._equation_list:
            if name in eq.get_name_set():
                return eq

    def clon(self):
        return deepcopy(self)

    def get_equation_that_contains_name_set(self, variable_name_set):
        for eq in self._equation_list:
            if eq.get_name_set().issuperset(variable_name_set):
                return eq

    def equal(self, other):
        if len(self._equation_list) != len(other._equation_list):
            return False
        found_equations = []
        for eq in self._equation_list:
            if eq in other._equation_list:
                found_equations.append(eq)
        return len(found_equations) == len(self._equation_list)

    def __eq__(self, other):
        if not isinstance(other, EquationSystem):
            return NotImplemented
        else:
            return self.equal(other)

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __str__(self):
        return '\n'.join(str(equation) for equation in self._equation_list)

    def __repr__(self):
        return 'EquationSystem([' + ', '.join(repr(equation) for equation in self._equation_list) + '])'
