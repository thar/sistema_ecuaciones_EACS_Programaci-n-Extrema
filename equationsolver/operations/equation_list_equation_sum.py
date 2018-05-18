from equationsolver.operations.equation_list_operation_applier import EquationListOperationApplier
from equationsolver.operations.equation_sum import EquationSum


class EquationListEquationSum(EquationListOperationApplier):
    def __init__(self, equation):
        EquationListOperationApplier.__init__(self, EquationSum(equation))
