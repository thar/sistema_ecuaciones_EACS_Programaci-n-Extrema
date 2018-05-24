from equationsolver.constant import Constant
from equationsolver.fraction import Fraction


class ConstantBuilder:
    def __init__(self):
        self._value = Fraction(1, 1)

    def value(self, value_arg):
        if isinstance(value_arg, Fraction):
            self._value = Fraction(value_arg._num, value_arg._den)
        else:
            self._value = Fraction(value_arg, 1)
        return self

    def build(self):
        return Constant(self._value)
