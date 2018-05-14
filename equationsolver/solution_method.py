class SolutionMethod:
    def __init__(self):
        self._equation_system = None

    def set(self, equation_system):
        self._equation_system = equation_system

    def resolve(self):
        raise NotImplemented
