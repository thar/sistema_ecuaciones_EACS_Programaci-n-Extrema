from equationsolver.term import Term
from copy import deepcopy


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
