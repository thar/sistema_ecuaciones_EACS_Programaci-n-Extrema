import unittest

from equationsolver.equation_builder import EquationBuilder
from equationsolver.equation_system_builder import EquationSystemBuilder


class EquationSystemTestCase(unittest.TestCase):
    def testEqualsEquationSystem(self):
        eq_system = EquationSystemBuilder().build()
        eq_system.add(EquationBuilder.one_equals_x())
        eq_system.add(EquationBuilder.y_equals_1())
        eq_system2 = eq_system.clon()
        self.assertEqual(eq_system, eq_system2)

    def testEqualsEquationSystem2(self):
        eq_system = EquationSystemBuilder().build()
        eq_system.add(EquationBuilder.y_equals_1())
        eq_system.add(EquationBuilder.one_equals_x())
        eq_system2 = eq_system.clon()
        self.assertEqual(eq_system, eq_system2)

    def testEqualsEquationSystem3(self):
        eq_system = EquationSystemBuilder().build()
        eq_system.add(EquationBuilder.y_equals_1())
        eq_system.add(EquationBuilder.one_equals_x())
        eq_system2 = eq_system.clon()
        eq_system.add(EquationBuilder().left_variable('z', 1, 0).right_default_constant().build())
        self.assertNotEqual(eq_system, eq_system2)

    # add and get_name_set test
    def testGivenEmptySystemWhenAddEquationWithXThenXisPresent(self):
        eq_system = EquationSystemBuilder().build()
        eq_system.add(EquationBuilder.x_equals_1())
        self.assertEqual(eq_system.get_name_set(), {'x'})

    def testGivenEmptySystemWhenAddEquationWithXAndAddWithYThenXAndYarePresent(self):
        eq_system = EquationSystemBuilder().build()
        eq_system.add(EquationBuilder.one_equals_x())
        eq_system.add(EquationBuilder.y_equals_1())
        self.assertEqual(eq_system.get_name_set(), {'x', 'y'})

    def testStrEquationSystem(self):
        eq_system = EquationSystemBuilder().build()
        eq_system.add(EquationBuilder.one_equals_x())
        eq_system.add(EquationBuilder.y_equals_1())
        self.assertEqual(str(eq_system), '+1 = +x\n+y = +1')

    def testReprEquationSyetem(self):
        eq_system = EquationSystemBuilder().build()
        eq_system.add(EquationBuilder.one_equals_x())
        eq_system.add(EquationBuilder.y_equals_1())
        self.assertEqual(repr(eq_system), 'EquationSystem([Equation(Expression([Constant(Fraction(1, 1))]), Expression([Variable(\'x\', Fraction(1, 1))])), Equation(Expression([Variable(\'y\', Fraction(1, 1))]), Expression([Constant(Fraction(1, 1))]))])')
