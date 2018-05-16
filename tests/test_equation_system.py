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

    # set and resolve test
    def testGivenEquationSystemAndSolutionMethodMockWhenSetAndResolveThenSolutionMethodMockResolveIsCalled(self):
        eq_system = EquationSystemBuilder().equation(EquationBuilder.x_equals_1()).build()
        solution_method = Mock(SolutionMethod)
        solution_method.resolve.side_effect = lambda: eq_system.set_solution('x', EquationBuilder.x_equals_1())
        eq_system.set(solution_method)
        eq_system.resolve()
        solution_method.resolve.assert_called_once()
