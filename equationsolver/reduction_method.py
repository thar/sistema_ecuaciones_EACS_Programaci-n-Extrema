from equationsolver.equation import Side
from equationsolver.solution_method import SolutionMethod


class ReductionMethod(SolutionMethod):
    def __init__(self):
        SolutionMethod.__init__(self)
        self._variable_to_reduce = None
        self._common_multiple = 1.0
        self._equation_to_resolve = None
        self._equation_system_to_recurse = None

    def resolve(self):
        self._equation_system.simplify()
        self._equation_system.pop_solution_equations()
        name_set = self._equation_system.get_name_set()
        if len(name_set) == 0:
            return
        self._variable_to_reduce = name_set.pop()
        self._equation_system.move_variable_to_side(self._variable_to_reduce, Side.left)
        self._equation_system.simplify()
        if len(name_set) > 0:
            self._resolve_recursive()
        else:
            self._equation_to_resolve = self._equation_system.get_equation_that_contains_name_set(
                {self._variable_to_reduce}).clon()
        self._compute_solution()

    def _compute_solution(self):
        self._equation_to_resolve.isolate_variable(self._variable_to_reduce)
        self._equation_system.set_solution(self._variable_to_reduce, self._equation_to_resolve)

    def _resolve_recursive(self):
        self._equation_system_to_recurse = self._equation_system.clon()
        self._get_reducible_variable_common_multiple()
        self._multiply_equations_to_reach_common_multiple()
        self._store_equation_to_reduce()
        self._reduce_all_equations()
        self._equation_system.simplify()
        self._equation_system_to_recurse.simplify()
        reduction_method = ReductionMethod()
        reduction_method.set(self._equation_system_to_recurse)
        reduction_method.resolve()
        self.merge_solutions()

    def _get_reducible_variable_common_multiple(self):
        self._equation_system_to_recurse.normalize()
        reducible_variable_values = self._equation_system_to_recurse.get_variable_name_values(Side.left,
                                                                                              self._variable_to_reduce)
        self._common_multiple = 1.0
        for value in reducible_variable_values:
            if value != 0:
                self._common_multiple *= value
        self._common_multiple = abs(self._common_multiple)

    def _multiply_equations_to_reach_common_multiple(self):
        self._equation_system_to_recurse.normalize()
        reducible_variable_values = self._equation_system_to_recurse.get_variable_name_values(Side.left,
                                                                                              self._variable_to_reduce)
        multiply_values = []
        for i in range(len(reducible_variable_values)):
            value = reducible_variable_values[i]
            if value != 0:
                multiply_values.append(self._common_multiple / value)
            else:
                multiply_values.append(1.0)
        self._equation_system_to_recurse.multiply_by_list(multiply_values)

    def _store_equation_to_reduce(self):
        self._equation_to_resolve = self._equation_system_to_recurse.get_equation_that_contains_name_set(
            {self._variable_to_reduce}).clon()

    def _reduce_all_equations(self):
        eq_to_reduce = self._equation_to_resolve.clon()
        eq_to_reduce.multiply(-1.0)
        self._equation_system_to_recurse.add_operation(eq_to_reduce)

    def merge_solutions(self):
        for variable_name in self._equation_system_to_recurse.get_solutions_name_set():
            variable_solution_equation = self._equation_system_to_recurse.get_solution(variable_name)
            variable_solution_value = variable_solution_equation.get_value_constant(Side.right)
            self._equation_system.set_solution(variable_name, variable_solution_equation)
            if variable_name in self._equation_to_resolve.get_name_set():
                self._equation_to_resolve.apply(variable_name, variable_solution_value)
        self._equation_to_resolve.simplify()

