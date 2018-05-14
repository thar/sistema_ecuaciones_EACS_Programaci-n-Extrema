from equationsolver.term_equality_analyzer import TermEqualityAnalyzer


class Term:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def multiply(self, value):
        self._value *= value

    def has_name(self, name):
        return False

    def has_name_set(self, name_set):
        return False

    def equal(self, other):
        term_equality_analyzer = TermEqualityAnalyzer(self, other)
        return term_equality_analyzer.is_equal()

    def clon(self):
        raise NotImplemented

    def dispatch(self, term_visitor):
        raise NotImplemented
