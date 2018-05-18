from equationsolver.operations.equation_list_operation_applier import EquationListOperationApplier
from equationsolver.operations.equation_simplify import EquationSimplify


class EquationListSimplify(EquationListOperationApplier):
    def __init__(self):
        EquationListOperationApplier.__init__(self, EquationSimplify())
