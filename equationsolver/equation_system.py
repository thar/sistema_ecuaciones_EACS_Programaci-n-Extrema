from copy import deepcopy

from equationsolver.equation import Side, Equation
from equationsolver.operations.equation_list_operation_applier import EquationListOperationApplier


class EquationSystem:
    def __init__(self):
        self._equation_list = []

    def add(self, equation):
        self._equation_list.append(equation.clon())

    def get_name_set(self):
        name_set = set()
        for equation in self._equation_list:
            name_set.update(equation.get_name_set())
        return name_set

    def apply_operation(self, operation):
        operation(self._equation_list)

    def normalize(self):
        self.apply_operation(EquationListOperationApplier(Equation.Normalizer()))

    def get_equation_with_name(self, name):
        for eq in self._equation_list:
            if name in eq.get_name_set():
                return eq

    def pop_solution_equations(self):
        temporal_equations = []
        found_solutions = {}
        for eq in self._equation_list:
            if eq.is_solution_equation():
                solved_variable = eq.get_name_set().pop()
                eq.apply_operation(Equation.VariableIsolator(solved_variable))
                found_solutions[solved_variable] = eq
            else:
                temporal_equations.append(eq)
        self._equation_list = temporal_equations
        self.apply_solutions(found_solutions)
        return found_solutions

    def apply_solutions(self, solutions):
        for eq in self._equation_list:
            for variable_name, solution_eq in solutions.iteritems():
                eq.apply_operation(Equation.ValueApplier(variable_name, solution_eq.get_value_constant(Side.right)))

    def clon(self):
        return deepcopy(self)

    def get_variable_name_values(self, side, name):
        values = []
        for eq in self._equation_list:
            values.append(eq.get_value_variable(side, name))
        return values

    def multiply_by_list(self, values_list):
        for i in range(len(values_list)):
            self._equation_list[i].apply_operation(Equation.ValueMultiplier(values_list[i]))

    def get_equation_that_contains_name_set(self, variable_name_set):
        for eq in self._equation_list:
            if eq.get_name_set().issuperset(variable_name_set):
                return eq

    def __str__(self):
        return '\n'.join(str(equation) for equation in self._equation_list)
