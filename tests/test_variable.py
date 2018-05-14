import unittest

from equationsolver.term_visitor import TermVisitor
from equationsolver.variable import Variable


class TermVisitorMock(TermVisitor):
    def __init__(self):
        TermVisitor.__init__(self)
        self._constant_call_count = 0
        self._variable_call_count = 0

    def visit_constant(self, variable):
        self._constant_call_count += 1

    def visit_variable(self, variable):
        self._variable_call_count += 1

    @property
    def visit_constant_count(self):
        return self._constant_call_count

    @property
    def visit_variable_count(self):
        return self._variable_call_count

    @property
    def total_count(self):
        return self.visit_constant_count + self.visit_variable_count


class VariableTestCase(unittest.TestCase):

    def testValue(self):
        variable = Variable('x', 3.0)
        self.assertEqual(variable.value, 3.0)

    def testMultiply(self):
        variable = Variable('x', 3.0)
        variable.multiply(2.0)
        self.assertEqual(variable.value, 6.0)

    def testEqual(self):
        variable1 = Variable('x', 3.0)
        variable2 = Variable('x', 3.0)
        self.assertTrue(variable1.equal(variable2))

    def testClon(self):
        variable1 = Variable('x', 3.0)
        variable2 = variable1.clon()
        self.assertFalse(variable1 is variable2)
        self.assertTrue(variable1.equal(variable2))

    def testHasNamePositive(self):
        variable1 = Variable('x', 3.0)
        self.assertTrue(variable1.has_name('x'))

    def testHasNameNegative(self):
        variable1 = Variable('x', 3.0)
        self.assertFalse(variable1.has_name('y'))

    def testHasNameSetPositive(self):
        variable1 = Variable('x', 3.0)
        name_set = ['x', 'y']
        self.assertTrue(variable1.has_name_set(name_set))

    def testHasNameSetNegative(self):
        variable1 = Variable('x', 3.0)
        name_set = ['z', 'y']
        self.assertFalse(variable1.has_name_set(name_set))

    def testDispatcher(self):
        variable1 = Variable('x', 3.0)
        term_visitor = TermVisitorMock()
        variable1.dispatch(term_visitor)
        self.assertEqual(term_visitor.visit_variable_count, 1)
        self.assertEqual(term_visitor.total_count, 1)
