from equationsolver.equation import Side
from equationsolver.operations.equation_list_operation_applier import EquationListOperationApplier
from equationsolver.equation import Equation


class EquationListSimplify(EquationListOperationApplier):
    def __init__(self):
        EquationListOperationApplier.__init__(self, Equation.EquationSimplifyer())

    def apply(self):
        EquationListOperationApplier.apply(self)
        self._remove_unneded_expressions()

    def _remove_unneded_expressions(self):
        unnedded_expressions = []
        for eq in self._equation_list:
            if len(eq.get_name_set()) == 0 and eq.get_value_constant(Side.left) == eq.get_value_constant(Side.right):
                unnedded_expressions.append(eq)
        for eq in unnedded_expressions:
            self._equation_list.remove(eq)
