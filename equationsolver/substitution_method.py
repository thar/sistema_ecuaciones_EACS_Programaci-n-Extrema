from equationsolver.equation import Equation
from equationsolver.equation_list_operation.equation_list_operation_applier import EquationListOperationApplier
from equationsolver.recursive_solution_method import RecursiveSolutionMethod


class SubstitutionMethod(RecursiveSolutionMethod):
    def __init__(self):
        RecursiveSolutionMethod.__init__(self)

    def _preprocess_input_equation_system(self):
        pass

    def _resolve_recursive(self):
        equation_system_to_recurse = self._equation_system.clon()
        equation_system_to_recurse.remove(self._equation_to_resolve)
        equation_system_to_recurse.apply_operation(
            EquationListOperationApplier(
                Equation.EquationApplier(self._variable_to_reduce, self._equation_to_resolve)))
        self._solution_method_recurse = SubstitutionMethod()
        self._solution_method_recurse.set(equation_system_to_recurse)
        self._solution_method_recurse.resolve()
