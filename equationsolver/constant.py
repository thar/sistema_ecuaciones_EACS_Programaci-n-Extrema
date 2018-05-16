from equationsolver.term import Term
from copy import deepcopy

from equationsolver.term_equality_analyzer import TermEqualityAnalyzer


class Constant(Term):
    def __init__(self, value):
        Term.__init__(self, value)

    def clon(self):
        return deepcopy(self)

    def dispatch(self, term_visitor):
        term_visitor.visit_constant(self)

    def equal(self, other):
        term_equality_analyzer = TermEqualityAnalyzer(self, other)
        return term_equality_analyzer.is_equal()

    def __str__(self):
        sign = '+' if self.value >= 0 else ''
        return sign + str(self.value)
