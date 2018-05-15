import unittest

from equationsolver.constant_builder import ConstantBuilder
from equationsolver.equation import Side
from equationsolver.equation_builder import EquationBuilder
from equationsolver.expression import EmptyExpression, NotSimplified
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
        equation.simplify_name(Side.left, term.name)
        self.assertEqual(equation.get_value_side(Side.left), 0.0)
        self.assertEqual(equation.get_name_set(), {term.name})
        equation.add_side(Side.right, inverse_term)
        equation.simplify_name(Side.right, term.name)
        self.assertEqual(equation.get_value_side(Side.right), 0.0)
        self.assertEqual(equation.get_name_set(), set())

    def testGivenEmptyEquationWhenAddConstantThenItIsAddedInBothSides(self):
        equation = EquationBuilder().build()
        term = ConstantBuilder().build()
        equation.add(term)
        self.assertEqual(equation.get_value_side(Side.left), term.value)
        self.assertEqual(equation.get_value_side(Side.right), term.value)

    # add_side tests
    def testGivenEmptyEquationWhenAddConstantSideLeftThenItIsAddedInLeftSides(self):
        equation = EquationBuilder().build()
        term = ConstantBuilder().build()
        equation.add_side(Side.left, term)
        self.assertEqual(equation.get_value_side(Side.left), term.value)
        self.assertRaises(EmptyExpression, equation.get_value_side, Side.right)

    def testGivenEmptyEquationWhenAddConstantSideRightThenItIsAddedInRightSides(self):
        equation = EquationBuilder().build()
        term = ConstantBuilder().build()
        equation.add_side(Side.right, term)
        self.assertEqual(equation.get_value_side(Side.right), term.value)
        self.assertRaises(EmptyExpression, equation.get_value_side, Side.left)

    # add_equation tests
    def testGivenEmptyEquationWhenAddEquationThenEquationIsEqualToAddedEquation(self):
        equation1 = EquationBuilder().build()
        equation2 = EquationBuilder.x_equals_1()
        equation1.add_equation(equation2)
        self.assertTrue(equation1.equal(equation2))

    def testGivenXIs0EquationWhenAddOIsYEquationThenYIsXEquationIsObtained(self):
        equation = EquationBuilder.x_equals_0()
        equation.add_equation(EquationBuilder.zero_equals_y())
        expected_equation = EquationBuilder().left_term(VariableBuilder().name('x').value(1.0).build()).left_term(
            ConstantBuilder().value(0).build()).right_term(ConstantBuilder().value(0).build()).right_term(
            VariableBuilder().name('y').value(1.0).build()).build()
        self.assertTrue(equation.equal(expected_equation))

    # multiply tests
    def testGivenDefaultEquationWhenMultiplyBy1ThenSameEquationIsObtained(self):
        equation1 = EquationBuilder.x_equals_1()
        equation2 = EquationBuilder.x_equals_1()
        equation1.multiply(1.0)
        self.assertTrue(equation1.equal(equation2))

    def testGivenDefaultEquationWhenMultiplyBy0ThenValue0IsObtainedInBothTerms(self):
        equation = EquationBuilder.x_equals_1()
        equation.multiply(0.0)
        self.assertRaises(LookupError, equation.get_value, 'x')
        self.assertEqual(equation.get_value_side(Side.left), 0.0)
        self.assertEqual(equation.get_value_side(Side.right), 0.0)

    # get_value tests
    def testGivenEmptyEquationWhenGetValueThenRaisesLookupError(self):
        equation = EquationBuilder().build()
        self.assertRaises(LookupError, equation.get_value, 'x')

    def testGivenEquationWithOneVariableAtLeftWhenGetValueThenVariableValueIsReturned(self):
        variable = VariableBuilder().build()
        equation = EquationBuilder().left_term(variable).right_default_constant().build()
        self.assertEqual(equation.get_value(variable.name), variable.value)

    def testGivenEquationWithOneVariableAtRightWhenGetValueThenVariableValueIsReturned(self):
        variable = VariableBuilder().build()
        equation = EquationBuilder().right_term(variable).left_default_constant().build()
        self.assertEqual(equation.get_value(variable.name), variable.value)

    def testGivenEquationWithSameVariableAtBothSidesWhenGetValueThenRaisesNotSimplified(self):
        equation = EquationBuilder().build()
        variable = VariableBuilder().build()
        equation.add(variable)
        self.assertRaises(NotSimplified, equation.get_value, variable.name)

    def testGivenEquationWithSameVariableTwiceAtLeftSidesWhenGetValueThenRaisesNotSimplified(self):
        variable = VariableBuilder().build()
        equation = EquationBuilder().left_term(variable).left_term(variable).right_default_constant().build()
        self.assertRaises(NotSimplified, equation.get_value, variable.name)

    def testGivenEquationWithSameVariableTwiceAtRightSidesWhenGetValueThenRaisesNotSimplified(self):
        variable = VariableBuilder().build()
        equation = EquationBuilder().right_term(variable).right_term(variable).left_default_constant().build()
        self.assertRaises(NotSimplified, equation.get_value, variable.name)

    # get_value_side tests
    def testGivenEmptyEquationWhenGetValueSideThenRaisesEmptyExpression(self):
        equation = EquationBuilder().build()
        self.assertRaises(EmptyExpression, equation.get_value_side, Side.left)
        self.assertRaises(EmptyExpression, equation.get_value_side, Side.right)

    def testGivenEquationWithOneConstantAtLeftWhenGetValueThenConstantValueIsReturned(self):
        constant = ConstantBuilder().build()
        equation = EquationBuilder().left_term(constant).build()
        self.assertEqual(equation.get_value_side(Side.left), constant.value)

    def testGivenEquationWithOneConstantAtRightWhenGetValueThenConstantValueIsReturned(self):
        constant = ConstantBuilder().build()
        equation = EquationBuilder().right_term(constant).build()
        self.assertEqual(equation.get_value_side(Side.right), constant.value)

    def testGivenEquationWithSameConstantTwiceAtLeftSidesWhenGetValueThenRaisesNotSimplified(self):
        constant = ConstantBuilder().build()
        equation = EquationBuilder().left_term(constant).left_term(constant).build()
        self.assertRaises(NotSimplified, equation.get_value_side, Side.left)

    def testGivenEquationWithSameConstantTwiceAtRightSidesWhenGetValueThenRaisesNotSimplified(self):
        constant = ConstantBuilder().build()
        equation = EquationBuilder().right_term(constant).right_term(constant).build()
        self.assertRaises(NotSimplified, equation.get_value_side, Side.right)

    # simplify_name tests
    @unittest.skip("Expression is not raising exceptions on simplify_name")
    def testGivenEmptyEquationWhenSimplifyNameThenEmptyExpressionIsRaised(self):
        equation = EquationBuilder().build()
        self.assertRaises(EmptyExpression, equation.simplify_name, Side.left, 'x')
        self.assertRaises(EmptyExpression, equation.simplify_name, Side.right, 'x')

    @unittest.skip("Expression is not raising exceptions on simplify")
    def testGivenEquationWithoutVariableWithNameXWhenSimplifyNameXThenLookupErrorIsRaised(self):
        equation = EquationBuilder.y_equals_1()
        self.assertRaises(LookupError, equation.simplify_name, Side.left, 'x')
        self.assertRaises(LookupError, equation.simplify_name, Side.right, 'x')

    def testGivenEquationSameVariableTwiceAtLeftWithNameXWhenSimplifyNameXThenVariableIsSimplified(self):
        term = VariableBuilder().build()
        equation = EquationBuilder().left_term(term).left_term(term).right_default_constant().build()
        equation.simplify_name(Side.left, term.name)
        self.assertEqual(equation.get_value(term.name), 2 * term.value)

    def testGivenEquationSameVariableTwiceAtRightWithNameXWhenSimplifyNameXThenVariableIsSimplified(self):
        term = VariableBuilder().build()
        equation = EquationBuilder().right_term(term).right_term(term).left_default_constant().build()
        equation.simplify_name(Side.right, term.name)
        self.assertEqual(equation.get_value(term.name), 2 * term.value)

    # simplify tests
    @unittest.skip("Expression is not raising exceptions on simplify_name")
    def testGivenEmptyEquationWhenSimplifyThenEmptyExpressionIsRaised(self):
        equation = EquationBuilder().build()
        self.assertRaises(EmptyExpression, equation.simplify, Side.left)
        self.assertRaises(EmptyExpression, equation.simplify, Side.right)

    @unittest.skip("Expression is not raising exceptions on simplify")
    def testGivenEquationWithoutConstantWhenSimplifyThenLookupErrorIsRaised(self):
        equation = EquationBuilder().left_default_variable().right_default_variable().build()
        self.assertRaises(LookupError, equation.simplify, Side.left)
        self.assertRaises(LookupError, equation.simplify, Side.right)

    def testGivenEquationSameConstantTwiceAtLeftWhenSimplifyThenConstantIsSimplified(self):
        term = ConstantBuilder().build()
        equation = EquationBuilder().left_term(term).left_term(term).build()
        equation.simplify(Side.left)
        self.assertEqual(equation.get_value_side(Side.left), 2 * term.value)

    def testGivenEquationSameConstantTwiceAtRightWhenSimplifyThenConstantIsSimplified(self):
        term = ConstantBuilder().build()
        equation = EquationBuilder().right_term(term).right_term(term).build()
        equation.simplify(Side.right)
        self.assertEqual(equation.get_value_side(Side.right), 2 * term.value)

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
        self.assertTrue(EquationBuilder.x_equals_1().equal(EquationBuilder.one_equals_x()))
