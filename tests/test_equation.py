import unittest

from equationsolver.constant_builder import ConstantBuilder
from equationsolver.equation import Side, Equation
from equationsolver.equation_builder import EquationBuilder
from equationsolver.expression import NotSimplified
from equationsolver.variable_builder import VariableBuilder


class EquationTestCase(unittest.TestCase):
    # add tests
    def testGivenEmptyEquationWhenAddTermThenTermIsAddedInBothSides(self):
        equation = EquationBuilder().build()
        term = VariableBuilder().build()
        inverse_term = term.clon()
        inverse_term.multiply(-1.0)
        equation.add(term)
        self.assertEqual(equation.get_name_set(), {term.name})
        equation.add_side(Side.left, inverse_term)
        equation.simplify_variable(Side.left, term.name)
        self.assertEqual(equation.get_value_constant(Side.left), 0.0)
        self.assertEqual(equation.get_name_set(), {term.name})
        equation.add_side(Side.right, inverse_term)
        equation.simplify_variable(Side.right, term.name)
        self.assertEqual(equation.get_value_constant(Side.right), 0.0)
        self.assertEqual(equation.get_name_set(), set())

    def testGivenEmptyEquationWhenAddConstantThenItIsAddedInBothSides(self):
        equation = EquationBuilder().build()
        term = ConstantBuilder().build()
        equation.add(term)
        self.assertEqual(equation.get_value_constant(Side.left), term.value)
        self.assertEqual(equation.get_value_constant(Side.right), term.value)

    # add_side tests
    def testGivenEmptyEquationWhenAddConstantSideLeftThenItIsAddedInLeftSide(self):
        equation = EquationBuilder().build()
        term = ConstantBuilder().value(1.0).build()
        equation.add_side(Side.left, term)
        self.assertEqual(equation.get_value_constant(Side.left), term.value)

    def testGivenEmptyEquationWhenAddConstantSideRightThenItIsAddedInRightSide(self):
        equation = EquationBuilder().build()
        term = ConstantBuilder().value(1.0).build()
        equation.add_side(Side.right, term)
        self.assertEqual(equation.get_value_constant(Side.right), term.value)

    # add_equation tests
    def testGivenEmptyEquationWhenAddEquationThenEquationIsEqualToAddedEquation(self):
        equation1 = EquationBuilder().build()
        equation2 = EquationBuilder.x_equals_1()
        equation1.add_equation(equation2)
        self.assertTrue(equation1.equal(equation2))
        self.assertTrue(equation1 == equation2)

    def testGivenXIs0EquationWhenAddOIsYEquationThenYIsXEquationIsObtained(self):
        equation = EquationBuilder.x_equals_0()
        equation.add_equation(EquationBuilder.zero_equals_y())
        expected_equation = EquationBuilder().left_term(VariableBuilder().name('x').value(1.0).build()).left_term(
            ConstantBuilder().value(0).build()).right_term(ConstantBuilder().value(0).build()).right_term(
            VariableBuilder().name('y').value(1.0).build()).build()
        self.assertTrue(equation.equal(expected_equation))

    def testGivenXIs1EquationAndXIs0WhenAskedForEqualityThenFalseIsReturned(self):
        equation1 = EquationBuilder.x_equals_0()
        equation2 = EquationBuilder.x_equals_1()
        self.assertFalse(equation1.equal(equation2))
        self.assertFalse(equation1 == equation2)
        self.assertTrue(equation1 != equation2)

    # multiply tests
    def testGivenDefaultEquationWhenMultiplyBy1ThenSameEquationIsObtained(self):
        equation1 = EquationBuilder.x_equals_1()
        equation2 = EquationBuilder.x_equals_1()
        equation1.multiply(1.0)
        self.assertTrue(equation1.equal(equation2))

    def testGivenDefaultEquationWhenMultiplyBy0ThenValue0IsObtainedInBothTerms(self):
        equation = EquationBuilder.x_equals_1()
        equation.multiply(0.0)
        self.assertEqual(equation.get_name_set(), set())
        self.assertEqual(equation.get_value_constant(Side.left), 0.0)
        self.assertEqual(equation.get_value_constant(Side.right), 0.0)

    # get_value tests
    def testGivenEmptyEquationWhenGetValueThen0IsReturned(self):
        equation = EquationBuilder().build()
        self.assertEqual(equation.get_value_variable(Side.left, 'x'), 0.0)
        self.assertEqual(equation.get_value_variable(Side.right, 'x'), 0.0)

    def testGivenEquationWithOneVariableAtLeftWhenGetValueThenVariableValueIsReturned(self):
        variable = VariableBuilder().build()
        equation = EquationBuilder().left_term(variable).right_default_constant().build()
        self.assertEqual(equation.get_value_variable(Side.left, variable.name), variable.value)

    def testGivenEquationWithOneVariableAtRightWhenGetValueThenVariableValueIsReturned(self):
        variable = VariableBuilder().build()
        equation = EquationBuilder().right_term(variable).left_default_constant().build()
        self.assertEqual(equation.get_value_variable(Side.right, variable.name), variable.value)

    def testGivenEquationWithSameVariableTwiceAtLeftSidesWhenGetValueThenRaisesNotSimplified(self):
        variable = VariableBuilder().build()
        equation = EquationBuilder().left_term(variable).left_term(variable).right_default_constant().build()
        self.assertRaises(NotSimplified, equation.get_value_variable, Side.left, variable.name)

    def testGivenEquationWithSameVariableTwiceAtRightSidesWhenGetValueThenRaisesNotSimplified(self):
        variable = VariableBuilder().build()
        equation = EquationBuilder().right_term(variable).right_term(variable).left_default_constant().build()
        self.assertRaises(NotSimplified, equation.get_value_variable, Side.right, variable.name)

    # get_value_side tests
    def testGivenEmptyEquationWhenGetValueSideThenReturns0(self):
        equation = EquationBuilder().build()
        self.assertEqual(equation.get_value_constant(Side.left), 0)
        self.assertEqual(equation.get_value_constant(Side.right), 0)

    def testGivenEquationWithOneConstantAtLeftWhenGetValueThenConstantValueIsReturned(self):
        constant = ConstantBuilder().build()
        equation = EquationBuilder().left_term(constant).build()
        self.assertEqual(equation.get_value_constant(Side.left), constant.value)

    def testGivenEquationWithOneConstantAtRightWhenGetValueThenConstantValueIsReturned(self):
        constant = ConstantBuilder().build()
        equation = EquationBuilder().right_term(constant).build()
        self.assertEqual(equation.get_value_constant(Side.right), constant.value)

    def testGivenEquationWithSameConstantTwiceAtLeftSidesWhenGetValueThenRaisesNotSimplified(self):
        constant = ConstantBuilder().build()
        equation = EquationBuilder().left_term(constant).left_term(constant).build()
        self.assertRaises(NotSimplified, equation.get_value_constant, Side.left)

    def testGivenEquationWithSameConstantTwiceAtRightSidesWhenGetValueThenRaisesNotSimplified(self):
        constant = ConstantBuilder().build()
        equation = EquationBuilder().right_term(constant).right_term(constant).build()
        self.assertRaises(NotSimplified, equation.get_value_constant, Side.right)

    # simplify_name tests
    def testGivenEquationSameVariableTwiceAtLeftWithNameXWhenSimplifyNameXThenVariableIsSimplified(self):
        term = VariableBuilder().build()
        equation = EquationBuilder().left_term(term).left_term(term).right_default_constant().build()
        equation.simplify_variable(Side.left, term.name)
        self.assertEqual(equation.get_value_variable(Side.left, term.name), 2 * term.value)

    def testGivenEquationSameVariableTwiceAtRightWithNameXWhenSimplifyNameXThenVariableIsSimplified(self):
        term = VariableBuilder().build()
        equation = EquationBuilder().right_term(term).right_term(term).left_default_constant().build()
        equation.simplify_variable(Side.right, term.name)
        self.assertEqual(equation.get_value_variable(Side.right, term.name), 2 * term.value)

    # simplify tests
    def testGivenEquationSameConstantTwiceAtLeftWhenSimplifyThenConstantIsSimplified(self):
        term = ConstantBuilder().build()
        equation = EquationBuilder().left_term(term).left_term(term).build()
        equation.simplify_constant(Side.left)
        self.assertEqual(equation.get_value_constant(Side.left), 2 * term.value)

    def testGivenEquationSameConstantTwiceAtRightWhenSimplifyThenConstantIsSimplified(self):
        term = ConstantBuilder().build()
        equation = EquationBuilder().right_term(term).right_term(term).build()
        equation.simplify_constant(Side.right)
        self.assertEqual(equation.get_value_constant(Side.right), 2 * term.value)

    # get_name_set tests
    def testGivenEmptyEquationWhenGetNameSetThenEmptyNameSetIsReturned(self):
        equation = EquationBuilder().build()
        self.assertEqual(equation.get_name_set(), set())

    def testGivenEquationWithConstantsWhenGetNameSetThenEmptyNameSetIsReturned(self):
        equation = EquationBuilder().left_default_constant().right_default_constant().build()
        self.assertEqual(equation.get_name_set(), set())

    def testGivenXEqualsOneEquationWhenGetNameSetThenEmptyNameSetWithXOnlyIsReturned(self):
        equation = EquationBuilder.x_equals_1()
        self.assertEqual(equation.get_name_set(), {'x'})

    def testGivenOneEqualsXEquationWhenGetNameSetThenEmptyNameSetWithXOnlyIsReturned(self):
        equation = EquationBuilder.one_equals_x()
        self.assertEqual(equation.get_name_set(), {'x'})

    def testGivenYEqualsXEquationWhenGetNameSetThenEmptyNameSetWithXAndYIsReturned(self):
        equation = EquationBuilder.y_equals_x()
        self.assertEqual(equation.get_name_set(), {'x', 'y'})

    # equal tests
    def testGivenXEqualsOneWhenEqualsAgainstOneEqualsXThenTrueIsReturned(self):
        self.assertTrue(EquationBuilder.x_equals_1().equal(EquationBuilder.one_equals_x()))

    def testGivenXEqualsOneWhenEqualsAgainstXEqualsOneThenTrueIsReturned(self):
        self.assertTrue(EquationBuilder.x_equals_1().equal(EquationBuilder.x_equals_1()))

    def testGivenXEqualsOneWhenEqualsAgainstYEqualsOneThenFalseIsReturned(self):
        self.assertFalse(EquationBuilder.x_equals_1().equal(EquationBuilder.y_equals_1()))

    # clon tests
    def testGivenXEqualsOneEquationWhenClonThenEquationEqualsReturnsTrue(self):
        equation = EquationBuilder.x_equals_1()
        equation_clon = equation.clon()
        self.assertFalse(equation is equation_clon)
        self.assertTrue(equation.equal(equation_clon))

    # apply tests
    def testGivenYEqualsXWhenApply1ToXThenYEqualsOneIsObtained(self):
        equation = EquationBuilder.y_equals_x()
        equation.apply('x', 1.0)
        self.assertTrue(equation.equal(EquationBuilder.y_equals_1()))

    def testGivenXEqualsYWhenApply1ToXThenYEqualsOneIsObtained(self):
        equation = EquationBuilder.y_equals_x()
        equation.invert()
        equation.apply('x', 1.0)
        self.assertTrue(equation.equal(EquationBuilder.y_equals_1()))

    def testGivenYEqualsXWhenApply1ToZThenLookupErrorIsRaised(self):
        equation = EquationBuilder.y_equals_x()
        self.assertRaises(LookupError, equation.apply, 'z', 1.0)

    def testGivenEmptyEquationWhenApplyThenLookupErrorIsRaised(self):
        equation = EquationBuilder().build()
        self.assertRaises(LookupError, equation.apply, 'z', 1.0)

    # invert tests
    def testGivenXEqualsOneEquationWhenInvertThenEquationOneEqualsXIsReturned(self):
        eq = EquationBuilder.x_equals_1()
        eq.invert()
        self.assertEqual(eq.get_value_constant(Side.left), 1.0)

    # EquationSimplifyer
    def testEquationSimplifyer(self):
        eq = EquationBuilder().left_constant(1).left_variable('x', 2, 1).left_variable('x', 1, 2).right_default_constant().build()
        eq.apply_operation(Equation.EquationSimplifyer())
        simplified_eq = EquationBuilder().left_constant(1).left_variable('x', 5, 2).right_default_constant().build()
        self.assertEqual(eq, simplified_eq)

    # VariableIsolator
    def testVariableIsolator(self):
        eq = EquationBuilder().left_constant(1).left_variable('x', 2, 1).right_variable('x', 1, 2).build()
        eq.apply_operation(Equation.VariableIsolator('x'))
        isolated_eq = EquationBuilder().left_variable('x', 1, 1).right_constant_fraction(-2, 3).build()
        self.assertEqual(eq, isolated_eq)

    def testVariableIsolatorWithMoreVariables(self):
        eq = EquationBuilder().left_constant(1).left_variable('x', 2, 1).left_variable('y', 1, 1).right_variable('x', 1, 1).build()
        eq.apply_operation(Equation.VariableIsolator('x'))
        isolated_eq = EquationBuilder().left_variable('x', 1, 1).right_constant(-1).right_variable('y', -1, 1).build()
        self.assertEqual(eq, isolated_eq)

    # Normalizer
    def testNormalizer(self):
        # TODO
        pass

    # ConstantMover
    def testConstantMover(self):
        # TODO
        pass

    # VariableMover
    def testVariableMover(self):
        # TODO
        pass

    # VariableSubstitutor
    def testVariableSubstitutor(self):
        # 1 + 2x + y = x
        eq = EquationBuilder().left_constant(1).left_variable('x', 2, 1).left_variable('y', 1, 1).right_variable('x', 1, 1).build()
        # 1 +x -y = y +1  ->  x = y + y  ->  x = 2y
        eq2 = EquationBuilder().left_constant(1).left_variable('x', 1, 1).left_variable('y', -1, 1).right_variable('y', 1, 1).right_constant_fraction(1, 1).build()
        # eq: 1 + 4y + y = 2y
        eq.apply_operation(Equation.VariableSubstitutor('x', eq2))
        resultant_eq = EquationBuilder().left_constant(1).left_variable('y', 4, 1).left_variable('y', 1, 1).right_variable('y', 2, 1).build()
        self.assertEqual(eq, resultant_eq)

    def testStrEquation(self):
        self.assertEqual(str(EquationBuilder.x_equals_1()), '+x = +1')

    def testReprEquation(self):
        self.assertEqual(repr(EquationBuilder.x_equals_1()), 'Equation(Expression([Variable(\'x\', Fraction(1, 1))]), Expression([Constant(Fraction(1, 1))]))')
