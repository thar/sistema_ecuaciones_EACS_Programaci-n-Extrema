from equationsolver.term import Term
from copy import deepcopy


class Constant(Term):
    def __init__(self, value):
        Term.__init__(self, value)

    def equal(self, other):
        return self._value == other._value

    def clon(self):
        return deepcopy(self)

    def dispatch(self, term_visitor):
        term_visitor.visit_constant(self)
