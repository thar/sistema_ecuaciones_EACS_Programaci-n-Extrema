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
        raise NotImplemented

    def clon(self):
        raise NotImplemented

    def dispatch(self, term_visitor):
        raise NotImplemented
