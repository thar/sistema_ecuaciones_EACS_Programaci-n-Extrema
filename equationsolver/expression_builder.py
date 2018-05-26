from equationsolver.expression import Expression
from constant_builder import ConstantBuilder
from variable_builder import VariableBuilder


class ExpressionBuilder:
    def __init__(self):
        self._terms_list = []

    def term(self, term_arg):
        self._terms_list.append(term_arg)
        return self

    def variable(self, name, value):
        self._terms_list.append(VariableBuilder().name(name).fraction(value, 1).build())
        return self

    def constant(self, value):
        self._terms_list.append(ConstantBuilder().fraction(value, 1).build())
        return self

    def default_constant(self):
        self._terms_list.append(ConstantBuilder().build())
        return self

    def default_variable(self):
        self._terms_list.append(VariableBuilder().build())
        return self

    def constant_fraction(self, num, den):
        self._terms_list.append(ConstantBuilder().fraction(num, den).build())
        return self

    def variable_fraction(self, name, num, den):
        self._terms_list.append(VariableBuilder().name(name).fraction(num, den).build())
        return self

    def build(self):
        expression = Expression()
        for term in self._terms_list:
            expression.add_term(term)
        return expression
