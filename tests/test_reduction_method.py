import unittest

from equationsolver.constant_builder import ConstantBuilder
from equationsolver.equation_builder import EquationBuilder
from equationsolver.equation_system_builder import EquationSystemBuilder
from equationsolver.equation_system_solver import EquationSystemSolver
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
        reduction_method = ReductionMethod()
        equation_system_solver = EquationSystemSolver(eqs, reduction_method)
        eqs.set_equation_system_solver(equation_system_solver)
        equation_system_solver.resolve()
        self.assertTrue(equation_system_solver.get_solution('x').equal(EquationBuilder.x_equals_1()))
        self.assertTrue(equation_system_solver.get_solution('y').equal(EquationBuilder.y_equals_1()))
        self.assertTrue(equation_system_solver.get_solution('z').equal(EquationBuilder().left_term(VariableBuilder().name('z').build()).right_term(ConstantBuilder().value(2).build()).build()))
