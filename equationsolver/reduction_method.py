from equationsolver.equation import Side, Equation
from equationsolver.operations.common_multiple_variable_setter import CommonMultipleVariableSetter
from equationsolver.operations.equation_list_operation_applier import EquationListOperationApplier
from equationsolver.operations.equation_list_simplify import EquationListSimplify
from equationsolver.recursive_solution_method import RecursiveSolutionMethod
from equationsolver.solution_method import SolutionMethod


class ReductionMethod(RecursiveSolutionMethod):
    def __init__(self):
        SolutionMethod.__init__(self)
        self._variable_to_reduce = None
        self._common_multiple = 1.0
        self._equation_to_resolve = None
        self._equation_to_reduce = None
        self._solution_method_recurse = None

    def _preprocess_input_equation_system(self):
        self._equation_system.apply_operation(
            EquationListOperationApplier(Equation.VariableMover(self._variable_to_reduce, Side.left)))
        self._equation_system.apply_operation(EquationListSimplify())

    def _resolve_last_iteration(self):
        self._equation_to_resolve = self._equation_system.get_equation_that_contains_name_set(
            {self._variable_to_reduce}).clon()

    def _resolve_recursive(self):
        equation_system_to_recurse = self._equation_system.clon()
        equation_system_to_recurse.apply_operation(CommonMultipleVariableSetter(self._variable_to_reduce))
        self._store_equation_to_reduce(equation_system_to_recurse)
        self._reduce_all_equations(equation_system_to_recurse)
        equation_system_to_recurse.apply_operation(EquationListSimplify())
        self._solution_method_recurse = ReductionMethod()
        self._solution_method_recurse.set(equation_system_to_recurse)
        self._solution_method_recurse.resolve()

    def _store_equation_to_reduce(self, equation_system_to_recurse):
        self._equation_to_reduce = equation_system_to_recurse.get_equation_that_contains_name_set(
            {self._variable_to_reduce}).clon()

    def _reduce_all_equations(self, equation_system_to_recurse):
        self._equation_to_reduce.multiply(-1.0)
        equation_system_to_recurse.apply_operation(EquationListOperationApplier(Equation.SumEquation(self._equation_to_reduce)))
