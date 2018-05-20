class EquationListOperation:
    def __init__(self):
        self._equation_list = None

    def set_equation_list(self, equation_list):
        self._equation_list = equation_list

    def __call__(self, equation_system):
        self.set_equation_list(equation_system._equation_list)
        self.apply()

    def apply(self):
        raise NotImplemented