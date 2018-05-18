class EquationSystemSolver:
    def __init__(self, equation_system, solution_method):
        self._equation_system = equation_system
        self._solution_method = solution_method

    def resolve(self):
        self._equation_system.resolve2()
