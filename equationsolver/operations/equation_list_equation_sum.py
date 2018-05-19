from equationsolver.operations.equation_list_operation_applier import EquationListOperationApplier
from equationsolver.equation import Equation


class EquationListEquationSum(EquationListOperationApplier):
    def __init__(self, equation):
        EquationListOperationApplier.__init__(self, Equation.SumEquation(equation))
