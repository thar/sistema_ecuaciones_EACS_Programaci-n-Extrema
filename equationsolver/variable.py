from equationsolver.term import Term
from copy import deepcopy

from equationsolver.term_equality_analyzer import TermEqualityAnalyzer


class Variable(Term):
    def __init__(self, name, value):
        Term.__init__(self, value)
        self._name = name

    @property
    def name(self):
        return self._name

    def has_name(self, name):
        return self._name == name

    def has_name_set(self, name_set):
        return self._name in name_set

    def clon(self):
        return deepcopy(self)

    def dispatch(self, term_visitor):
        term_visitor.visit_variable(self)

    def equal(self, other):
        term_equality_analyzer = TermEqualityAnalyzer(self, other)
        return term_equality_analyzer.is_equal()

    def __str__(self):
        if self.value < 0:
            value_string = '-'
        else:
            value_string = '+'
        self_absolute_value = abs(self.value)
        if self_absolute_value != 1:
            if self.value % 1 == 0 or self_absolute_value == 0:
                value_string += str(self_absolute_value)
            else:
                value_string += '(' + str(self_absolute_value) + ')'
            return value_string + '*' + self.name
        else:
            return value_string + self.name

    def __repr__(self):
        return 'Variable(\'' + self._name + '\', ' + repr(self._value) + ')'
