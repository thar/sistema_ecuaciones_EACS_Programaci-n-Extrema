class TermVisitor:

    def __init__(self):
        pass

    def visit_variable(self, variable):
        raise NotImplemented

    def visit_constant(self, variable):
        raise NotImplemented
