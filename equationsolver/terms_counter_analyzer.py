from equationsolver.term_visitor import TermVisitor


class TermsCounterAnalyzer(TermVisitor):
    def __init__(self, terms_list):
        TermVisitor.__init__(self)
        self.count_map = {'constant': []}
        self.terms_list = terms_list
        for term in self.terms_list:
            term.dispatch(self)

    def visit_constant(self, constant):
        self.count_map['constant'].append(constant)

    def visit_variable(self, variable):
        if variable.name in self.count_map:
            self.count_map[variable.name].append(variable)
        else:
            self.count_map[variable.name] = [variable]

    def get_constants(self):
        return self.count_map['constant']

    def get_variables(self):
        variables_array = []
        for variable_name, variables in self.count_map.iteritems():
            if variable_name != 'constant':
                variables_array.extend(variables)
        return variables_array

    def get_variables_count(self):
        return len(self.get_variables())

    def get_variables_with_name(self, name):
        if name in self.count_map:
            return self.count_map[name]
        else:
            return []

    def get_constant_count(self):
        return len(self.get_constants())

    def get_variable_name_count(self, name):
        return len(self.get_variables_with_name(name))

    def get_variables_names_set(self):
        variables_names_dict = self.count_map.keys()
        variables_names_dict.remove('constant')
        return set(variables_names_dict)
