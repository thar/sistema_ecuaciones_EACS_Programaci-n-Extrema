import unittest

from equationsolver.constant_builder import ConstantBuilder
from equationsolver.equation_builder import EquationBuilder
from equationsolver.equation_system_builder import EquationSystemBuilder
from equationsolver.reduction_method import ReductionMethod
from equationsolver.variable_builder import VariableBuilder


class ReductionMethodTestCase(unittest.TestCase):
    def testGivenWhenThen0(self):
        eqs = EquationSystemBuilder().build()
        eqs.add(EquationBuilder.y_equals_x())
        a = EquationBuilder.one_equals_x()
        b = EquationBuilder().left_term(VariableBuilder().name('z').build()).right_term(VariableBuilder().name('x').build()).right_term(VariableBuilder().name('y').build()).build()
        a.add_equation(EquationBuilder.one_equals_y())
        eqs.add(a)
        eqs.add(b)
        eqs.set(ReductionMethod())
        eqs.resolve()
        self.assertTrue(eqs.get_solution('x').equal(EquationBuilder.x_equals_1()))
        self.assertTrue(eqs.get_solution('y').equal(EquationBuilder.y_equals_1()))
        self.assertTrue(eqs.get_solution('z').equal(EquationBuilder().left_term(VariableBuilder().name('z').build()).right_term(ConstantBuilder().value(2).build()).build()))
