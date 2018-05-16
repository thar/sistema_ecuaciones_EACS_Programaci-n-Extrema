class NotSolved(Exception):
    pass


class EquationSystem:
    def __init__(self):
        self._equation_list = []
        self._solutions = {}
        self._solution_method = None

    def add(self, equation):
        self._equation_list.append(equation.clon())

    def set(self, solution_method):
        self._solution_method = solution_method
        self._solution_method.set(self)

    def resolve(self):
        name_set = self.get_name_set()
        while set(self._solutions.keys()) != name_set:
            self._solution_method.resolve()

    def get_name_set(self):
        return self._get_equation_list_name_set(self._equation_list)

    def __get(self, index):
        return self._equation_list[index]

    def get_last_before(self, before):
        return self._equation_list[before - 1]

    def get_last(self):
        return self._equation_list[-1]

    def copy_before_before(self, before):
        self._equation_list = self._equation_list[:before] + self.__get(before).clon() + self._equation_list[before:]

    def copy_before(self):
        self.add(self.get_last())

    def set_solution(self, first_name, equation):
        self._solutions[first_name] = equation

    def _get_equation_list_name_set(self, equation_list):
        name_set = set()
        for equation in equation_list:
            name_set.update(equation.get_name_set())
        return name_set

    def get_solution(self, name):
        if name not in self._solutions:
            raise NotSolved
        return self._solutions[name]

    def equal(self):
        return False

    def __str__(self):
        return '\n'.join(str(equation) for equation in self._equation_list)
