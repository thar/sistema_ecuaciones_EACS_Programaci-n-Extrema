from copy import deepcopy

from enum import Enum

from equationsolver.expression_builder import ExpressionBuilder


class Side(Enum):
    left = 1
    right = 2


class Equation:
    def __init__(self, left_expression=None, right_expression=None):
        if left_expression:
            self._left_expression = left_expression
        else:
            self._left_expression = ExpressionBuilder().build()
        if right_expression:
            self._right_expression = right_expression
        else:
            self._right_expression = ExpressionBuilder().build()

    def add(self, term):
        pass

    def add_side(self, side, term):
        pass

    def add_equation(self, equation):
        pass

    def multiply(self, value):
        pass

    def get_value(self, name):
        return 0.0

    def get_value_side(self, side):
        return 0.0

    def simplify_name(self, side, name):
        pass

    def simplify(self, side):
        pass

    def get_name_set(self):
        return ['x']

    def equal(self, equation):
        return False

    def clon(self):
        return deepcopy(self)

    def apply(self, name, value):
        pass

    def invert(self):
        pass
