import unittest

from equationsolver.variable import Variable


class VariableTestCase(unittest.TestCase):

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
