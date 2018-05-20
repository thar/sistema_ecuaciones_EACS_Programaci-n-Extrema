class EquationSystemSolver:
    def __init__(self, equation_system, solution_method):
        self._equation_system = equation_system
        self._solution_method = solution_method
        self._solution_method.set(self._equation_system)

    def resolve(self):
        self._solution_method.resolve()

    def get_solution(self, name):
        return self._solution_method.get_solution(name)
