from equationsolver.fraction import Fraction
from equationsolver.variable import Variable


class VariableBuilder:
    def __init__(self):
        self._name = 'x'
        self._value = Fraction(1, 1)

    def name(self, name_arg):
        self._name = name_arg
        return self

    def value(self, value_arg):
        if isinstance(value_arg, Fraction):
            self._value = Fraction(value_arg._num, value_arg._den)
        else:
            self._value = Fraction(value_arg, 1)
        return self

    def fraction(self, num, den):
        self._value = Fraction(num, den)
        return self

    def build(self):
        return Variable(self._name, self._value)
