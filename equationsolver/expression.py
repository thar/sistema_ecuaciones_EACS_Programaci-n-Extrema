from copy import deepcopy


class Expression:

    def __init__(self):
        pass

    def empty(self):
        return False

    def add_term(self):
        pass

    def add_expression(self):
        pass

    def multiply(self, value):
        pass

    def simplify(self, name):
        pass

    def get_value(self):
        return 0.0

    def get_value_name(self, name):
        return 0.0

    def get_name_set(self):
        return ['x']

    def has_name(self, name):
        return False

    def apply(self, name, value):
        pass

    def equal(self, expression):
        return False

    def clon(self):
        return deepcopy(self)
