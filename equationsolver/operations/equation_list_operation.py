class EquationListOperation:
    def __init__(self):
        self._equation_list = None

    def set_equation_list(self, equation_list):
        self._equation_list = equation_list

    def apply(self):
        raise NotImplemented