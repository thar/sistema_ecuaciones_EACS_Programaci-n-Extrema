from equationsolver.term import Term
from copy import deepcopy


class Variable(Term):
    def __init__(self, name, value):
        Term.__init__(self, value)
        self._name = name

    def has_name(self, name):
        return self._name == name

    def has_name_set(self, name_set):
        return self._name in name_set

    def equal(self, other):
        return self._name == other._name and self._value == other._value

    def clon(self):
        return deepcopy(self)

    def dispatch(self, term_visitor):
        term_visitor.visit_variable(self)
