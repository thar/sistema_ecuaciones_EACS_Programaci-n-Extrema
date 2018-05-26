from equationsolver.constant_builder import ConstantBuilder
from equationsolver.equation import Equation
from equationsolver.expression_builder import ExpressionBuilder
from equationsolver.variable_builder import VariableBuilder


class EquationBuilder:
    def __init__(self):
        self._left_expression = ExpressionBuilder().build()
        self._right_expression = ExpressionBuilder().build()

    def left_expression(self, left_expression):
        self._left_expression = left_expression
        return self

    def right_expression(self, right_expression):
        self._right_expression = right_expression
        return self

    def left_term(self, term):
        self._left_expression.add_term(term)
        return self

    def right_term(self, term):
        self._right_expression.add_term(term)
        return self

    def left_default_constant(self):
        self._left_expression.add_term(ConstantBuilder().build())
        return self

    def right_default_constant(self):
        self._right_expression.add_term(ConstantBuilder().build())
        return self

    def left_default_variable(self):
        self._left_expression.add_term(VariableBuilder().build())
        return self

    def right_default_variable(self):
        self._right_expression.add_term(VariableBuilder().build())
        return self

    @staticmethod
    def x_equals_1():
        return EquationBuilder().left_term(VariableBuilder().name('x').value(1).build()).right_term(
            ConstantBuilder().value(1).build()).build()

    @staticmethod
    def y_equals_1():
        return EquationBuilder().left_term(VariableBuilder().name('y').value(1).build()).right_term(
            ConstantBuilder().value(1).build()).build()

    @staticmethod
    def x_equals_0():
        return EquationBuilder().left_term(VariableBuilder().name('x').value(1).build()).right_term(
            ConstantBuilder().value(0).build()).build()

    @staticmethod
    def y_equals_0():
        return EquationBuilder().left_term(VariableBuilder().name('y').value(1).build()).right_term(
            ConstantBuilder().value(0).build()).build()

    @staticmethod
    def one_equals_x():
        return EquationBuilder().right_term(VariableBuilder().name('x').value(1).build()).left_term(
            ConstantBuilder().value(1).build()).build()

    @staticmethod
    def one_equals_y():
        return EquationBuilder().right_term(VariableBuilder().name('y').value(1).build()).left_term(
            ConstantBuilder().value(1).build()).build()

    @staticmethod
    def zero_equals_x():
        return EquationBuilder().right_term(VariableBuilder().name('x').value(1).build()).left_term(
            ConstantBuilder().value(0).build()).build()

    @staticmethod
    def zero_equals_y():
        return EquationBuilder().right_term(VariableBuilder().name('y').value(1).build()).left_term(
            ConstantBuilder().value(0).build()).build()

    @staticmethod
    def y_equals_x():
        return EquationBuilder().right_term(VariableBuilder().name('x').value(1).build()).left_term(
            VariableBuilder().name('y').value(1).build()).build()

    @staticmethod
    def zero_equals_zero():
        return EquationBuilder().left_term(ConstantBuilder().value(0).build()).right_term(
            ConstantBuilder().value(0).build()).build()

    def build(self):
        return Equation(left_expression=self._left_expression, right_expression=self._right_expression)
