import unittest
from mock import Mock

from equationsolver.equation_builder import EquationBuilder
from equationsolver.equation_system_builder import EquationSystemBuilder
from equationsolver.solution_method import SolutionMethod


class EquationSystemTestCase(unittest.TestCase):
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
