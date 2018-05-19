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

    class EquationSimplifyer(Operation):
        def __init__(self):
            Equation.Operation.__init__(self)

        def apply(self):
            for side in Side:
                self._equation.simplify_constant(side)
                for name in self._equation.get_name_set():
                    self._equation.simplify_variable(side, name)

    def __init__(self, left_expression=None, right_expression=None):
        self._expression = {}
        if left_expression:
            self._expression[Side.left] = left_expression
        else:
            self._expression[Side.left] = ExpressionBuilder().build()
        if right_expression:
            self._expression[Side.right] = right_expression
        else:
            self._expression[Side.right] = ExpressionBuilder().build()

    def apply_operation(self, op):
        op(self)

    def add_equation(self, equation):
        self.apply_operation(Equation.SumEquation(equation))

    def add(self, term):
        self.apply_operation(Equation.AddTermBothSides(term))

    def multiply(self, value):
        self.apply_operation(Equation.ValueMultiplier(value))

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

    def apply(self, name, value):
        if name not in self.get_name_set():
            raise LookupError
        for side in Side:
            if name in self._expression[side].get_name_set():
                self._expression[side].apply(name, value)

    def invert(self):
        new_expression = {
            Side.left: self._expression[Side.right],
            Side.right: self._expression[Side.left]
        }
        self._expression = new_expression

    def move_variable_to_side(self, name, side):
        side_to_remove_from = Side.right
        if side == Side.right:
            side_to_remove_from = Side.left
        variable_value = self.get_value_variable(side_to_remove_from, name)
        if variable_value != 0:
            self.add(VariableBuilder().name(name).value(-variable_value).build())

    def move_constant_to_side(self, side):
        side_to_remove_from = Side.right
        if side == Side.right:
            side_to_remove_from = Side.left
        constant_value = self.get_value_constant(side_to_remove_from)
        if constant_value != 0:
            self.add(ConstantBuilder().value(-constant_value).build())

    def is_solution_equation(self):
        return len(self.get_name_set()) == 1

    def normalize(self):
        self.move_constant_to_side(Side.right)
        for name in self.get_name_set():
            self.move_variable_to_side(name, Side.left)
        self.apply_operation(Equation.EquationSimplifyer())

    def isolate_variable(self, variable_name):
        self.apply_operation(Equation.EquationSimplifyer())
        self.move_constant_to_side(Side.right)
        for name in self.get_name_set():
            if name != variable_name:
                self.move_variable_to_side(name, Side.right)
            else:
                self.move_variable_to_side(variable_name, Side.left)
        self.apply_operation(Equation.EquationSimplifyer())
        self.multiply(1.0/self.get_value_variable(Side.left, name))
        self.apply_operation(Equation.EquationSimplifyer())

    def __str__(self):
        return str(self._expression[Side.left]) + ' = ' + str(self._expression[Side.right])
