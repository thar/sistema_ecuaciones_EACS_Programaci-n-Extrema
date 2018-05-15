from equationsolver.variable import Variable


class VariableBuilder:
    def __init__(self):
        self._name = 'x'
        self._value = 1.0

    def name(self, name_arg):
        self._name = name_arg
        return self

    def value(self, value_arg):
        self._value = value_arg
        return self

    def build(self):
        return Variable(self._name, self._value)
