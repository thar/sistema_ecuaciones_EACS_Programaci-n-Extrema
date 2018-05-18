from equationsolver.operations.equation_operation import EquationOperation


class EquationSum(EquationOperation):
    def __init__(self, equation):
        EquationOperation.__init__(self)
        self._equation_to_sum = equation

    def apply(self):
        self._equation.add_equation(self._equation_to_sum)
