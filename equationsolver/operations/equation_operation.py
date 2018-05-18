class EquationOperation:
    def __init__(self):
        self._equation = None

    def set_equation(self, equation):
        self._equation = equation

    def apply(self):
        raise NotImplemented
