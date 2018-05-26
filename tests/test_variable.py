import unittest
from mock import patch, Mock

from equationsolver.fraction import Fraction
from equationsolver.variable_builder import VariableBuilder


class VariableTestCase(unittest.TestCase):

    def testValue(self):
        variable = VariableBuilder().value(3.0).build()
        self.assertEqual(variable.value, 3.0)

    def testMultiply(self):
        variable = VariableBuilder().value(3.0).build()
        variable.multiply(2.0)
        self.assertEqual(variable.value, 6.0)

    def testEqualPositive(self):
        variable1 = VariableBuilder().name('x').value(3.0).build()
        variable2 = VariableBuilder().name('x').value(3.0).build()
        self.assertTrue(variable1.equal(variable2))

    def testEqualNegativeValue(self):
        variable1 = VariableBuilder().name('x').value(3.0).build()
        variable2 = VariableBuilder().name('x').value(3.1).build()
        self.assertFalse(variable1.equal(variable2))
        self.assertNotEqual(variable1, variable2)

    def testEqualNegativeName(self):
        variable1 = VariableBuilder().name('x').value(3.0).build()
        variable2 = VariableBuilder().name('y').value(3.0).build()
        self.assertFalse(variable1.equal(variable2))
        self.assertNotEqual(variable1, variable2)

    def testEqualNegativeValueAndName(self):
        variable1 = VariableBuilder().name('x').value(3.0).build()
        variable2 = VariableBuilder().name('y').value(3.1).build()
        self.assertFalse(variable1.equal(variable2))
        self.assertNotEqual(variable1, variable2)

    def testEqualWithConstantSameValueNegative(self):
        variable1 = VariableBuilder().value(3.0).build()
        variable2 = Mock()
        variable2.value = 3.0
        variable2.dispatch = Mock(side_effect=lambda x: x.visit_constant(variable2))
        self.assertFalse(variable1.equal(variable2))
        self.assertNotEqual(variable1, variable2)

    def testEqualWithConstantDifferentValueNegative(self):
        variable1 = VariableBuilder().value(3.0).build()
        variable2 = Mock()
        variable2.value = 2.0
        variable2.dispatch = Mock(side_effect=lambda x: x.visit_constant(variable2))
        self.assertFalse(variable1.equal(variable2))
        self.assertNotEqual(variable1, variable2)

    def testClon(self):
        variable1 = VariableBuilder().build()
        variable2 = variable1.clon()
        self.assertFalse(variable1 is variable2)
        self.assertTrue(variable1.equal(variable2))

    def testHasNamePositive(self):
        variable1 = VariableBuilder().name('x').build()
        self.assertTrue(variable1.has_name('x'))

    def testHasNameNegative(self):
        variable1 = VariableBuilder().name('x').build()
        self.assertFalse(variable1.has_name('y'))

    def testHasNameSetPositive(self):
        variable1 = VariableBuilder().name('x').build()
        name_set = ['x', 'y']
        self.assertTrue(variable1.has_name_set(name_set))

    def testHasNameSetNegative(self):
        variable1 = VariableBuilder().name('x').build()
        name_set = ['z', 'y']
        self.assertFalse(variable1.has_name_set(name_set))

    def testStrVariable(self):
        self.assertEqual(str(VariableBuilder().name('x').value(Fraction(1, 2)).build()), '+(1/2)*x')
        self.assertEqual(str(VariableBuilder().name('x').value(Fraction(-1, 2)).build()), '-(1/2)*x')
        self.assertEqual(str(VariableBuilder().name('x').value(Fraction(1, 1)).build()), '+x')
        self.assertEqual(str(VariableBuilder().name('x').value(Fraction(-1, 1)).build()), '-x')
        self.assertEqual(str(VariableBuilder().name('x').value(Fraction(-4, 2)).build()), '-2*x')
        self.assertEqual(str(VariableBuilder().name('x').value(Fraction(4, 2)).build()), '+2*x')
        self.assertEqual(str(VariableBuilder().name('x').value(Fraction(0, 2)).build()), '+0*x')

    def testReprVariable(self):
        self.assertEqual(repr(VariableBuilder().name('x').value(Fraction(1, 2)).build()), 'Variable(\'x\', Fraction(1, 2))')

    @patch('equationsolver.term_visitor.TermVisitor')
    def testDispatcher(self, TermVisitor):
        variable1 = VariableBuilder().build()
        term_visitor = TermVisitor()
        variable1.dispatch(term_visitor)
        self.assertEqual(term_visitor.visit_variable.call_count, 1)
