class NotSolved(Exception):
    pass


class EquationSystem:
    def __init__(self):
        self._equation_list = []
        self._solutions = {}
        self._solution_method = None

    def add(self, equation):
        pass

    def set(self, solution_method):
        pass

    def resolve(self):
        pass

    def get_name_set(self):
        return None

    def __get(self, index):
        return None

    def get_last_before(self, before):
        return None

    def get_last(self):
        return None

    def copy_before_before(self, before):
        pass

    def copy_before(self):
        pass

    def set_solution(self, first_name, equation):
        pass

    def get_solution(self, name):
        raise NotSolved

    def equal(self):
        return False

    def __str__(self):
        return ''
