from copy import deepcopy

from equationsolver.constant_builder import ConstantBuilder
from equationsolver.terms_counter_analyzer import TermsCounterAnalyzer
from equationsolver.variable import Variable


class NotSimplified(Exception):
    pass


class Expression:

    def __init__(self):
        self._term_list = []

    def empty(self):
        return len(self._term_list) is 0

    def add_term(self, term):
        if len(self._term_list) == 0 or term.value != 0:
            self._term_list.append(term.clon())

    def add_expression(self, expression):
        for term in expression._term_list:
            self.add_term(term)

    def multiply(self, value):
        for term in self._term_list:
            term.multiply(value)
        if 0 == value:
            terms_counter_analyzer = TermsCounterAnalyzer(self._term_list)
            terms = terms_counter_analyzer.get_variables()
            self._remove_terms(terms)
            if 0 == len(self._term_list):
                self._term_list.append(ConstantBuilder().value(0).build())

    def _get_added_terms_value(self, terms):
        term_value = 0.0
        for term in terms:
            term_value += term.value
        return term_value

    def _remove_terms(self, terms):
        for term in terms:
            self._term_list.remove(term)

    def simplify_constant(self):
        terms_counter_analyzer = TermsCounterAnalyzer(self._term_list)
        terms = terms_counter_analyzer.get_constants()
        if 0 == len(terms):
            return
        self._remove_terms(terms)
        self.add_term(ConstantBuilder().value(self._get_added_terms_value(terms)).build())

    def simplify_variable(self, name):
        terms_counter_analyzer = TermsCounterAnalyzer(self._term_list)
        terms = terms_counter_analyzer.get_variables_with_name(name)
        if 0 == len(terms):
            return
        self._remove_terms(terms)
        variable_value = self._get_added_terms_value(terms)
        if 0 == variable_value:
            self.add_term(ConstantBuilder().value(variable_value).build())
        else:
            self.add_term(Variable(name, variable_value))

    def get_value_constant(self):
        terms_counter_analyzer = TermsCounterAnalyzer(self._term_list)
        constants = terms_counter_analyzer.get_constants()
        if 1 == len(constants):
            return constants[0].value
        elif 1 < len(constants):
            raise NotSimplified
        else:
            return 0

    def get_value_variable(self, name):
        terms_counter_analyzer = TermsCounterAnalyzer(self._term_list)
        terms = terms_counter_analyzer.get_variables_with_name(name)
        if 1 == len(terms):
            return terms[0].value
        elif 1 < len(terms):
            raise NotSimplified
        else:
            return 0

    def get_name_set(self):
        terms_counter_analyzer = TermsCounterAnalyzer(self._term_list)
        return terms_counter_analyzer.get_variables_names_set()

    def has_name(self, name):
        return name in self.get_name_set()

    def apply(self, name, value):
        terms_counter_analyzer = TermsCounterAnalyzer(self._term_list)
        terms = terms_counter_analyzer.get_variables_with_name(name)
        if len(terms) == 0:
            raise LookupError
        self._remove_terms(terms)
        for term in terms:
            term.multiply(value)
            self.add_term(ConstantBuilder().value(term.value).build())

    def equal(self, expression):
        for term1 in self._term_list:
            found = False
            for term2 in expression._term_list:
                if term1.equal(term2):
                    found = True
                    break
            if not found:
                return False
        return True

    def clon(self):
        return deepcopy(self)

    def __eq__(self, other):
        if not isinstance(other, Expression):
            return NotImplemented
        else:
            return self.equal(other)

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __str__(self):
        return ' '.join([str(term) for term in self._term_list])

    def __repr__(self):
        return 'Expression([' + ', '.join([repr(term) for term in self._term_list]) + '])'
