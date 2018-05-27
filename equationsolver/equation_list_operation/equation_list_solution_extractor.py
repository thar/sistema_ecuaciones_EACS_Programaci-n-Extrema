from equationsolver.equation import Equation
from equationsolver.equation_list_operation.equation_list_operation import EquationListOperation
from equationsolver.equation_list_operation.equation_list_operation_applier import EquationListOperationApplier


class EquationListSolutionExtractor(EquationListOperation):
    def __init__(self):
        EquationListOperation.__init__(self)
        self._found_solutions = {}

    def apply(self):
        equations_to_remove = []
        for eq in self._equation_list:
            if eq.is_solution_equation():
                solved_variable = eq.get_name_set().pop()
                eq.apply_operation(Equation.VariableIsolator(solved_variable))
                self._found_solutions[solved_variable] = eq
                equations_to_remove.append(eq)
        for eq in equations_to_remove:
            self._equation_list.remove(eq)
        solutions_appplier = EquationListOperationApplier(Equation.SolutionEquationsApplier(self._found_solutions))
        solutions_appplier.set_equation_list(self._equation_list)
        solutions_appplier.apply()

    @property
    def solutions(self):
        return self._found_solutions
