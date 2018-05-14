from equationsolver.constant import Constant


class ConstantBuilder:
    def __init__(self):
        self._value = 1.0

    def value(self, value_arg):
        self._value = value_arg
        return self

    def build(self):
        return Constant(self._value)
