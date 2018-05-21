from equationsolver.equation import Side, Equation
from equationsolver.operations.common_multiple_variable_setter import CommonMultipleVariableSetter
from equationsolver.operations.equation_list_equation_sum import EquationListEquationSum
from equationsolver.operations.equation_list_operation_applier import EquationListOperationApplier
from equationsolver.operations.equation_list_simplify import EquationListSimplify
from equationsolver.solution_method import SolutionMethod


class ReductionMethod(SolutionMethod):
    def __init__(self):
        SolutionMethod.__init__(self)
        self._variable_to_reduce = None
        self._common_multiple = 1.0
        self._equation_to_resolve = None
        self._equation_to_reduce = None
        self._solution_method_recurse = None

    def resolve(self):
        self._equation_system.apply_operation(EquationListSimplify())
        self._solutions.update(self._equation_system.pop_solution_equations())
        name_set = self._equation_system.get_name_set()
        if len(name_set) == 0:
            return
        self._variable_to_reduce = name_set.pop()
        self._equation_system.apply_operation(
            EquationListOperationApplier(Equation.VariableMover(self._variable_to_reduce, Side.left)))
        self._equation_system.apply_operation(EquationListSimplify())
        self._store_equation_to_resolve()
        if len(name_set) > 0:
            self._resolve_recursive()
            self.merge_solutions()
        else:
            self._equation_to_resolve = self._equation_system.get_equation_that_contains_name_set(
                {self._variable_to_reduce}).clon()
        self._compute_solution()

    def _compute_solution(self):
        self._equation_to_resolve.apply_operation(Equation.VariableIsolator(self._variable_to_reduce))
        self.set_solution(self._variable_to_reduce, self._equation_to_resolve)

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

    def _store_equation_to_resolve(self):
        self._equation_to_resolve = self._equation_system.get_equation_that_contains_name_set(
            {self._variable_to_reduce}).clon()

    def _reduce_all_equations(self, equation_system_to_recurse):
        self._equation_to_reduce.multiply(-1.0)
        equation_system_to_recurse.apply_operation(EquationListEquationSum(self._equation_to_reduce))

    def merge_solutions(self):
        for variable_name in self._solution_method_recurse.get_solutions_name_set():
            variable_solution_equation = self._solution_method_recurse.get_solution(variable_name)
            variable_solution_value = variable_solution_equation.get_value_constant(Side.right)
            self.set_solution(variable_name, variable_solution_equation)
            if variable_name in self._equation_to_resolve.get_name_set():
                self._equation_to_resolve.apply_operation(Equation.ValueApplier(variable_name, variable_solution_value))
        self._equation_to_resolve.apply_operation(Equation.EquationSimplifyer())
