from equationsolver.constant_builder import ConstantBuilder
from equationsolver.equation import Side
from equationsolver.equation_builder import EquationBuilder
from equationsolver.equation_system_builder import EquationSystemBuilder
from equationsolver.solution_method import SolutionMethod
from equationsolver.variable_builder import VariableBuilder


class ReductionMethod(SolutionMethod):
    def __init__(self):
        SolutionMethod.__init__(self)
        self._equation_list = []
        self._variable_to_reduce = None
        self._common_multiple = 1.0
        self._equation_to_resolve = None

    def resolve(self):
        self._equation_system.simplify()
        self._equation_system.pop_solution_equations()
        self._grab_needed_equations()
        name_set = self._equation_system.get_name_set()
        if len(name_set) == 0:
            return 
        self._variable_to_reduce = name_set.pop()
        self._equation_system.move_variable_to_side(self._variable_to_reduce, Side.left)
        self._equation_system.simplify()
        if len(name_set) > 0:
            self._resolve_recursive(name_set)
        else:
            self._store_equation_to_reduce()
        self._compute_solution()

    def _compute_solution(self):
        self._equation_to_resolve.isolate_variable(self._variable_to_reduce)
        self._equation_system.set_solution(self._variable_to_reduce, self._equation_to_resolve)

    def _resolve_recursive(self, name_set):
        self._get_reducible_variable_common_multiple()
        self._multiply_equations_to_reach_common_multiple()
        self._store_equation_to_reduce()
        self._reduce_all_equations()
        self._remove_zero_equal_zero_equations()
        new_equation_system = self._create_new_equation_system()
        reduction_method = ReductionMethod()
        reduction_method.set(new_equation_system)
        reduction_method.resolve()
        for variable_name in name_set:
            variable_solution_equation = new_equation_system.get_solution(variable_name)
            variable_solution_value = variable_solution_equation.get_value_constant(Side.right)
            self._equation_system.set_solution(variable_name, variable_solution_equation)
            if variable_name in self._equation_to_resolve.get_name_set():
                self._equation_to_resolve.apply(variable_name, variable_solution_value)
        self._equation_to_resolve.simplify()

    def _grab_needed_equations(self):
        self._equation_list = self._equation_system.get_equation_list()

    def _get_name_set(self):
        name_set = set()
        for eq in self._equation_list:
            name_set.update(eq.get_name_set())
        return name_set

    def _get_reducible_variable_common_multiple(self):
        self._common_multiple = 1.0
        for eq in self._equation_list:
            value = eq.get_value_variable(Side.left, self._variable_to_reduce)
            if value != 0:
                self._common_multiple *= value
        self._common_multiple = abs(self._common_multiple)

    def _multiply_equations_to_reach_common_multiple(self):
        for eq in self._equation_list:
            if self._variable_to_reduce in eq.get_name_set():
                eq.multiply(self._common_multiple/eq.get_value_variable(Side.left, self._variable_to_reduce))

    def _store_equation_to_reduce(self):
        for eq in self._equation_list:
            if self._variable_to_reduce in eq.get_name_set():
                self._equation_to_resolve = eq.clon()
                return

    def _reduce_all_equations(self):
        eq_to_reduce = self._equation_to_resolve.clon()
        eq_to_reduce.multiply(-1.0)
        for eq in self._equation_list:
            eq.add_equation(eq_to_reduce)

    def _remove_zero_equal_zero_equations(self):
        new_equations = []
        for eq in self._equation_list:
            if not eq.equal(EquationBuilder.zero_equals_zero()):
                new_equations.append(eq)
        self._equation_list = new_equations

    def _create_new_equation_system(self):
        new_equation_system = EquationSystemBuilder().build()
        for eq in self._equation_list:
            new_equation_system.add(eq.clon())
        return new_equation_system

