from equationsolver.operations.equation_list_operation import EquationListOperation


class EquationListSimplify(EquationListOperation):
    def apply(self):
        for eq in self._equation_list:
            eq.simplify()