from copy import deepcopy

from enum import Enum

from equationsolver.expression import NotSimplified
from equationsolver.expression_builder import ExpressionBuilder


class Side(Enum):
    left = 1
    right = 2


class Equation:
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

    def add(self, term):
        self._expression[Side.left].add_term(term)
        self._expression[Side.right].add_term(term)

    def add_side(self, side, term):
        self._expression[side].add_term(term)

    def add_equation(self, equation):
        for side in Side:
            self._expression[side].add_expression(equation._expression[side])

    def multiply(self, value):
        for side in Side:
            self._expression[side].multiply(value)

    def get_value_variable(self, side, name):
        return self._expression[side].get_value_variable(name)

    def get_value_constant(self, side):
        return self._expression[side].get_value_constant()

    def simplify_name(self, side, name):
        self._expression[side].simplify_name(name)

    def simplify(self, side):
        self._expression[side].simplify()

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

    def __str__(self):
        return str(self._expression[Side.left]) + ' = ' + str(self._expression[Side.right])
