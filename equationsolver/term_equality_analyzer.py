from equationsolver.term_visitor import TermVisitor


class TermEqualityAnalyzer(TermVisitor):
    def __init__(self, term_a, term_b):
        TermVisitor.__init__(self)
        self._term_a = term_a
        self._term_b = term_b
        self._constant_seen = False
        self._variable_seen = False
        self._term_a.dispatch(self)
        self._term_b.dispatch(self)

    def visit_constant(self, variable):
        self._constant_seen = True

    def visit_variable(self, variable):
        self._variable_seen = True

    def is_equal(self):
        if self._constant_seen and self._variable_seen:
            return False
        elif self._constant_seen:
            return self._term_a.value == self._term_b.value
        elif self._variable_seen:
            return self._term_a.value == self._term_b.value and self._term_a.name == self._term_b.name