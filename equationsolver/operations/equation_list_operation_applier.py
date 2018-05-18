from equationsolver.operations.equation_list_operation import EquationListOperation


class EquationListOperationApplier(EquationListOperation):
    def __init__(self, operation):
        EquationListOperation.__init__(self)
        self._operation = operation

    def apply(self):
        for eq in self._equation_list:
            self._operation.set_equation(eq)
            self._operation.apply()
