from copy import deepcopy


class Equation:
    def __init__(self):
        pass

    def add(self, term):
        pass

    def add_side(self, side, term):
        pass

    def add_equation(self, equation):
        pass

    def multiply(self, value):
        pass

    def get_value(self, name):
        return 0.0

    def get_value_side(self, side):
        return 0.0

    def simplify_name(self, side, name):
        pass

    def simplify(self, side):
        pass

    def get_name_set(self):
        return ['x']

    def equal(self, equation):
        return False

    def clon(self):
        return deepcopy(self)

    def apply(self, name, value):
        pass

    def invert(self):
        pass
