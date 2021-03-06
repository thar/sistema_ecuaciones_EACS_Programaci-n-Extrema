import unittest
from mock import patch, Mock

from equationsolver.constant import Constant
from equationsolver.constant_builder import ConstantBuilder


class ConstantTestCase(unittest.TestCase):

    def testValue(self):
        variable = ConstantBuilder().value(3.0).build()
        self.assertEqual(variable.value, 3.0)

    def testMultiply(self):
        variable = ConstantBuilder().value(3.0).build()
        variable.multiply(2.0)
        self.assertEqual(variable.value, 6.0)

    def testEqualWithConstantPositive(self):
        variable1 = ConstantBuilder().value(3.0).build()
        variable2 = ConstantBuilder().value(3.0).build()
        self.assertTrue(variable1.equal(variable2))
        self.assertEqual(variable1, variable2)

    def testEqualWithConstantNegative(self):
        variable1 = ConstantBuilder().value(3.0).build()
        variable2 = ConstantBuilder().value(3.1).build()
        self.assertFalse(variable1.equal(variable2))
        self.assertNotEqual(variable1, variable2)

    def testEqualWithVariableSameValueNegative(self):
        variable1 = ConstantBuilder().value(2.0).build()
        variable2 = Mock()
        variable2.value = 2.0
        variable2.dispatch = Mock(side_effect=lambda x: x.visit_variable(variable2))
        self.assertFalse(variable1.equal(variable2))
        self.assertNotEqual(variable1, variable2)

    def testEqualWithVariableDifferentValueNegative(self):
        variable1 = ConstantBuilder().value(3.0).build()
        variable2 = Mock()
        variable2.value = 3.1
        variable2.dispatch = Mock(side_effect=lambda x: x.visit_variable(variable2))
        self.assertFalse(variable1.equal(variable2))
        self.assertNotEqual(variable1, variable2)

    def testClon(self):
        variable1 = ConstantBuilder().build()
        variable2 = variable1.clon()
        self.assertFalse(variable1 is variable2)
        self.assertTrue(variable1.equal(variable2))

    def testHasNameNegative(self):
        variable1 = ConstantBuilder().build()
        self.assertFalse(variable1.has_name('x'))

    def testHasNameSetNegative(self):
        variable1 = ConstantBuilder().build()
        name_set = ['z', 'y']
        self.assertFalse(variable1.has_name_set(name_set))

    @patch('equationsolver.term_visitor.TermVisitor')
    def testDispatcher(self, TermVisitor):
        variable1 = ConstantBuilder().build()
        term_visitor = TermVisitor()
        variable1.dispatch(term_visitor)
        self.assertEqual(term_visitor.visit_constant.call_count, 1)
