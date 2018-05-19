from equationsolver.operations.equation_list_operation import EquationListOperation


class EquationListOperationApplier(EquationListOperation):
    def __init__(self, operation):
        EquationListOperation.__init__(self)
        self._operation = operation

    def apply(self):
        for eq in self._equation_list:
            eq.apply_operation(self._operation)

    def __call__(self, equation_system):
        self.set_equation_list(equation_system._equation_list)
        self.apply()
