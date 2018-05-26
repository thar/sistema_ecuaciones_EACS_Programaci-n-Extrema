from copy import deepcopy
from enum import Enum

from equationsolver.constant_builder import ConstantBuilder
from equationsolver.expression_builder import ExpressionBuilder
from equationsolver.variable_builder import VariableBuilder


class Side(Enum):
    left = 1
    right = 2


class Equation:
    class Operation:
        def __init__(self):
            self._equation = None

        def set_equation(self, equation):
            self._equation = equation

        def apply(self):
            raise NotImplemented

        def __call__(self, equation):
            self.set_equation(equation)
            self.apply()

    class AddTermBothSides(Operation):
        def __init__(self, term):
            Equation.Operation.__init__(self)
            self._term = term

        def apply(self):
            self._equation._expression[Side.left].add_term(self._term)
            self._equation._expression[Side.right].add_term(self._term)

    class SumEquation(Operation):
        def __init__(self, equation):
            Equation.Operation.__init__(self)
            self._equation_to_add = equation

        def apply(self):
            for side in Side:
                self._equation._expression[side].add_expression(self._equation_to_add._expression[side])

    class ValueMultiplier(Operation):
        def __init__(self, value):
            Equation.Operation.__init__(self)
            self._value = value

        def apply(self):
            for side in Side:
                self._equation._expression[side].multiply(self._value)

    class ValueApplier(Operation):
        def __init__(self, name, value):
            Equation.Operation.__init__(self)
            self._name = name
            self._value = value

        def apply(self):
            if self._name not in self._equation.get_name_set():
                raise LookupError
            for side in Side:
                if self._name in self._equation._expression[side].get_name_set():
                    self._equation._expression[side].apply(self._name, self._value)

    class TermMover(Operation):
        def __init__(self, side_to_move_to):
            Equation.Operation.__init__(self)
            self._term = None
            self._move_to = side_to_move_to
            self._remove_from = Side.right
            if self._move_to == Side.right:
                self._remove_from = Side.left

        def apply(self):
            self._init_term()
            if self._term.value != 0:
                self._equation.apply_operation(Equation.AddTermBothSides(self._term))

        def _init_term(self):
            raise NotImplemented

    class VariableMover(TermMover):
        def __init__(self, name, side_to_move_to):
            Equation.TermMover.__init__(self, side_to_move_to)
            self._name = name

        def _init_term(self):
            variable_value = self._equation.get_value_variable(self._remove_from, self._name)
            self._term = VariableBuilder().name(self._name).value(-variable_value).build()

    class ConstantMover(TermMover):
        def __init__(self, side_to_move_to):
            Equation.TermMover.__init__(self, side_to_move_to)

        def _init_term(self):
            self._term = ConstantBuilder().value(-self._equation.get_value_constant(self._remove_from)).build()

    class Normalizer(Operation):
        def __init__(self):
            Equation.Operation.__init__(self)

        def apply(self):
            self._equation.apply_operation(Equation.ConstantMover(Side.right))
            for name in self._equation.get_name_set():
                self._equation.apply_operation(Equation.VariableMover(name, Side.left))
            self._equation.apply_operation(Equation.EquationSimplifyer())

    class VariableIsolator(Operation):
        def __init__(self, variable_name):
            Equation.Operation.__init__(self)
            self._variable_name = variable_name

        def apply(self):
            self._equation.apply_operation(Equation.EquationSimplifyer())
            self._equation.apply_operation(Equation.ConstantMover(Side.right))
            for name in self._equation.get_name_set():
                if name != self._variable_name:
                    self._equation.apply_operation(Equation.VariableMover(name, Side.right))
                else:
                    self._equation.apply_operation(Equation.VariableMover(self._variable_name, Side.left))
            self._equation.apply_operation(Equation.EquationSimplifyer())
            self._equation.apply_operation(
                Equation.ValueMultiplier(1.0 / self._equation.get_value_variable(Side.left, self._variable_name)))
            self._equation.apply_operation(Equation.EquationSimplifyer())

    class EquationSimplifyer(Operation):
        def __init__(self):
            Equation.Operation.__init__(self)

        def apply(self):
            for side in Side:
                self._equation.simplify_constant(side)
                for name in self._equation.get_name_set():
                    self._equation.simplify_variable(side, name)

    class EquationInverter(Operation):
        def __init__(self):
            Equation.Operation.__init__(self)

        def apply(self):
            new_expression = {
                Side.left: self._equation._expression[Side.right],
                Side.right: self._equation._expression[Side.left]
            }
            self._equation._expression = new_expression

    def __init__(self, left_expression=None, right_expression=None):
        self._expression = {Side.left: ExpressionBuilder().build(),
                            Side.right: ExpressionBuilder().build()}
        if left_expression:
            self._expression[Side.left] = left_expression
        if right_expression:
            self._expression[Side.right] = right_expression

    def apply_operation(self, op):
        op(self)

    def add_equation(self, equation):
        self.apply_operation(Equation.SumEquation(equation))

    def add(self, term):
        self.apply_operation(Equation.AddTermBothSides(term))

    def multiply(self, value):
        self.apply_operation(Equation.ValueMultiplier(value))

    def apply(self, name, value):
        self.apply_operation(Equation.ValueApplier(name, value))

    def normalize(self):
        self.apply_operation(Equation.Normalizer())

    def invert(self):
        self.apply_operation(Equation.EquationInverter())

    def add_side(self, side, term):
        self._expression[side].add_term(term)

    def get_value_variable(self, side, name):
        return self._expression[side].get_value_variable(name)

    def get_value_constant(self, side):
        return self._expression[side].get_value_constant()

    def simplify_variable(self, side, name):
        self._expression[side].simplify_variable(name)

    def simplify_constant(self, side):
        self._expression[side].simplify_constant()

    def get_name_set(self):
        name_set = set()
        for side in Side:
            name_set.update(self._expression[side].get_name_set())
        return name_set

    def equal(self, equation):
        return (self._expression[Side.left].equal(equation._expression[Side.left]) and
                self._expression[Side.right].equal(equation._expression[Side.right])) \
               or (self._expression[Side.left].equal(equation._expression[Side.right]) and
                   self._expression[Side.right].equal(equation._expression[Side.left]))

    def clon(self):
        return deepcopy(self)

    def is_solution_equation(self):
        return len(self.get_name_set()) == 1

    def __str__(self):
        return str(self._expression[Side.left]) + ' = ' + str(self._expression[Side.right])

    def __repr__(self):
        return 'Equation(' + repr(self._expression[Side.left]) + ', ' + repr(self._expression[Side.right]) + ')'
