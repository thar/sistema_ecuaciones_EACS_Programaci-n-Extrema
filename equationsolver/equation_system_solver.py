class EquationSystemSolver:
    def __init__(self, equation_system, solution_method):
        self._equation_system = equation_system
        self._solution_method = solution_method
        self._solutions = {}

    def resolve(self):
        self._equation_system.resolve2()

    def set_solution(self, name, equation):
        self._solutions[name] = equation
