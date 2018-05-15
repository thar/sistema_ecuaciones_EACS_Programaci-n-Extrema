from equationsolver.term import Term
from copy import deepcopy


class Constant(Term):
    def __init__(self, value):
        Term.__init__(self, value)

    def clon(self):
        return deepcopy(self)

    def dispatch(self, term_visitor):
        term_visitor.visit_constant(self)

    def __str__(self):
        return str(self.value)
