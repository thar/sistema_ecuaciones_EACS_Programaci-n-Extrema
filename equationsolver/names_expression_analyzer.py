from equationsolver.term_visitor import TermVisitor


class NamesExpressionAnalyzer(TermVisitor):
    def __init__(self, term_list):
        TermVisitor.__init__(self)
        self,_term_list = term_list

    def visit_constant(self, variable):
        pass

    def visit_variable(self, variable):
        pass

    def get_name_set(self):
        return ['']
