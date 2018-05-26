from equationsolver.equation import Equation, Side
from equationsolver.equation_list_operation.equation_list_simplify import EquationListSimplify
from equationsolver.solution_method import SolutionMethod


class RecursiveSolutionMethod(SolutionMethod):
    def __init__(self):
        SolutionMethod.__init__(self)
        self._variable_to_reduce = None
        self._equation_to_resolve = None
        self._solution_method_recurse = None

    def resolve(self):
        self._equation_system.apply_operation(EquationListSimplify())
        self._solutions.update(self._equation_system.pop_solution_equations())
        name_set = self._equation_system.get_name_set()
        if len(name_set) == 0:
            return
        self._variable_to_reduce = name_set.pop()
        self._preprocess_input_equation_system()
        self._store_equation_to_resolve()
        if len(name_set) > 0:
            self._resolve_recursive()
            self._merge_solutions()
        else:
            self._resolve_last_iteration()
        self._compute_solution()

    def _preprocess_input_equation_system(self):
        raise NotImplemented

    def _resolve_recursive(self):
        raise NotImplemented

    def _resolve_last_iteration(self):
        raise NotImplemented

    def _store_equation_to_resolve(self):
        self._equation_to_resolve = self._equation_system.get_equation_that_contains_name_set(
            {self._variable_to_reduce}).clon()

    def _compute_solution(self):
        self._equation_to_resolve.apply_operation(Equation.VariableIsolator(self._variable_to_reduce))
        self.set_solution(self._variable_to_reduce, self._equation_to_resolve)

    def _merge_solutions(self):
        for variable_name in self._solution_method_recurse.get_solutions_name_set():
            variable_solution_equation = self._solution_method_recurse.get_solution(variable_name)
            variable_solution_value = variable_solution_equation.get_value_constant(Side.right)
            self.set_solution(variable_name, variable_solution_equation)
            if variable_name in self._equation_to_resolve.get_name_set():
                self._equation_to_resolve.apply_operation(Equation.ValueApplier(variable_name, variable_solution_value))
        self._equation_to_resolve.apply_operation(Equation.EquationSimplifyer())