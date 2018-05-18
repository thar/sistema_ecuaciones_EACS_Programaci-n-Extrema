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
        self._grab_needed_equations()
        self._equation_system.simplify()
        self._fix_already_solved_equations()
        name_set = self._get_name_set()
        if len(name_set) == 0:
            return 
        self._variable_to_reduce = name_set.pop()
        self._move_reducible_variable_to_left_side_in_all_equations(self._equation_list, self._variable_to_reduce)
        self._equation_system.simplify()
        if len(name_set) > 0:
            self._resolve_recursive(name_set)
        else:
            self._store_equation_to_reduce()
        self._compute_solution()

    def _compute_solution(self):
        ReductionMethod._move_constant_to_right_side(self._equation_to_resolve)
        ReductionMethod._move_reducible_variable_to_left_side(self._equation_to_resolve, self._variable_to_reduce)
        ReductionMethod._simplify_equation(self._equation_to_resolve)
        variable_value = self._equation_to_resolve.get_value_variable(Side.left, self._variable_to_reduce)
        self._equation_to_resolve.multiply(1.0/variable_value)
        self._equation_system.set_solution(self._variable_to_reduce, self._equation_to_resolve)

    def _resolve_recursive(self, name_set):
        self._get_reducible_variable_common_multiple()
        self._multiply_equations_to_reach_common_multiple()
        self._store_equation_to_reduce()
        self._reduce_all_equations()
        self._equation_system.simplify()
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
        ReductionMethod._simplify_equation(self._equation_to_resolve)

    def _grab_needed_equations(self):
        self._equation_list = []
        index = 1
        while self._get_name_set() != self._equation_system.get_name_set() or \
                        len(self._equation_list) < len(self._get_name_set()):
            self._equation_list.append(self._equation_system.get_last_before(index))
            index += 1

    def _get_name_set(self):
        name_set = set()
        for eq in self._equation_list:
            name_set.update(eq.get_name_set())
        return name_set

    @staticmethod
    def _simplify_equation(eq):
        for side in Side:
            eq.simplify_constant(side)
            for name in eq.get_name_set():
                eq.simplify_variable(side, name)

    @staticmethod
    def _move_reducible_variable_to_left_side_in_all_equations(equation_list, variable_name):
        for eq in equation_list:
            ReductionMethod._move_reducible_variable_to_left_side(eq, variable_name)

    @staticmethod
    def _move_reducible_variable_to_left_side(eq, variable_name):
        variable_value = eq.get_value_variable(Side.right, variable_name)
        if variable_value != 0:
            eq.add(VariableBuilder().name(variable_name).value(-variable_value).build())

    @staticmethod
    def _move_constant_to_right_side(eq):
        constant_value = eq.get_value_constant(Side.left)
        if constant_value != 0:
            eq.add(ConstantBuilder().value(-constant_value).build())

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

    def _fix_already_solved_equations(self):
        temp_equations = []
        solved_variables = {}
        for eq in self._equation_list:
            eq_name_set = eq.get_name_set()
            if len(eq_name_set) == 1:
                self._variable_to_reduce = eq_name_set.pop()
                self._equation_to_resolve = eq
                self._compute_solution()
                solved_variables[self._variable_to_reduce] = self._equation_to_resolve.get_value_constant(Side.right)
            else:
                temp_equations.append(eq)
        self._equation_list = temp_equations
        for solved_variable, solved_variable_value in solved_variables.iteritems():
            for eq in self._equation_list:
                eq.apply(solved_variable, solved_variable_value)
        if len(solved_variables) != 0:
            self._fix_already_solved_equations()

