from equationsolver.equation import Side
from equationsolver.operations.equation_operation import EquationOperation


class EquationSimplify(EquationOperation):
    def apply(self):
        for side in Side:
            self._equation.simplify_constant(side)
            for name in self._equation.get_name_set():
                self._equation.simplify_variable(side, name)
