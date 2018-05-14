import unittest
from mock import patch, Mock

from equationsolver.variable import Variable


class VariableTestCase(unittest.TestCase):

    def testValue(self):
        variable = Variable('x', 3.0)
        self.assertEqual(variable.value, 3.0)

    def testMultiply(self):
        variable = Variable('x', 3.0)
        variable.multiply(2.0)
        self.assertEqual(variable.value, 6.0)

    def testEqualPositive(self):
        variable1 = Variable('x', 3.0)
        variable2 = Variable('x', 3.0)
        self.assertTrue(variable1.equal(variable2))

    def testEqualNegativeValue(self):
        variable1 = Variable('x', 3.0)
        variable2 = Variable('x', 3.1)
        self.assertFalse(variable1.equal(variable2))

    def testEqualNegativeName(self):
        variable1 = Variable('x', 3.0)
        variable2 = Variable('y', 3.0)
        self.assertFalse(variable1.equal(variable2))

    def testEqualNegativeValueAndName(self):
        variable1 = Variable('x', 3.0)
        variable2 = Variable('y', 3.1)
        self.assertFalse(variable1.equal(variable2))

    def testEqualWithConstantSameValueNegative(self):
        variable1 = Variable('x', 3.0)
        variable2 = Mock()
        variable2.value = 3.0
        variable2.has_name = Mock(return_value=False)
        variable2.has_name_set = Mock(return_value=False)
        variable2.dispatch = Mock(side_effect=lambda x: x.visit_constant(variable2))
        self.assertFalse(variable1.equal(variable2))

    def testEqualWithConstantDifferentValueNegative(self):
        variable1 = Variable('x', 3.0)
        variable2 = Mock()
        variable2.value = 2.0
        variable2.has_name = Mock(return_value=False)
        variable2.has_name_set = Mock(return_value=False)
        variable2.dispatch = Mock(side_effect=lambda x: x.visit_constant(variable2))
        self.assertFalse(variable1.equal(variable2))

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

    @patch('equationsolver.term_visitor.TermVisitor')
    def testDispatcher(self, TermVisitor):
        variable1 = Variable('x', 3.0)
        term_visitor = TermVisitor()
        variable1.dispatch(term_visitor)
        self.assertEqual(term_visitor.visit_variable.call_count, 1)
