from equationsolver.constant_builder import ConstantBuilder
from equationsolver.equation_system import EquationSystem
from equationsolver.expression_builder import ExpressionBuilder
from equationsolver.variable_builder import VariableBuilder


class EquationSystemBuilder:
    def __init__(self):
        self._equations = []

    def equation(self, equation):
        self._equations.append(equation)
        return self

    def build(self):
        equation_system = EquationSystem()
        for equation in self._equations:
            equation_system.add(equation)
        return equation_system
