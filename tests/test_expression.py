import unittest

from equationsolver.constant_builder import ConstantBuilder
from equationsolver.expression import NotSimplified, EmptyExpression
from equationsolver.expression_builder import ExpressionBuilder
from equationsolver.variable_builder import VariableBuilder


class ExpressionTestCase(unittest.TestCase):
    # empty tests
    def testGivenEmptyExpressionWhenEmptyThenReturnsTrue(self):
        expression = ExpressionBuilder().build()
        self.assertTrue(expression.empty())

    def testGivenNotEmptyExpressionWhenEmptyThenReturnsFalse(self):
        expression = ExpressionBuilder().default_constant().build()
        self.assertFalse(expression.empty())

    # get_value tests
    def testGivenExpressionWithOnlyAConstantAsTermWhenGetValueThenConstantValueIsReturned(self):
        constant = ConstantBuilder().build()
        expression = ExpressionBuilder().build()
        expression.add_term(constant)
        self.assertEqual(expression.get_value(), constant.value)

    def testGivenExpressionWithOnlyAVariableAsTermWhenGetValueThenLookupErrorIsRaised(self):
        expression = ExpressionBuilder().default_variable().build()
        self.assertRaises(LookupError, expression.get_value)

    def testGivenEmptyExpressionWhenGetValueThenEmptyExpressionIsRaised(self):
        expression = ExpressionBuilder().build()
        self.assertRaises(EmptyExpression, expression.get_value)

    def testGivenExpressionWithConstantAndVariableWhenGetValueThenConstantValueIsReturned(self):
        constant = ConstantBuilder().build()
        expression = ExpressionBuilder().term(constant).default_variable().build()
        self.assertEqual(expression.get_value(), constant.value)

    def testGivenExpressionWithTwoConstantsWhenGetValueThenNotSimplifiedIsRaised(self):
        expression = ExpressionBuilder().default_constant().default_constant().build()
        self.assertRaises(NotSimplified, expression.get_value)

    # get_value_name tests
    def testGivenExpressionWithVariableWhenGetValueNameThenVariableValueIsReturned(self):
        variable = VariableBuilder().name('x').build()
        expression = ExpressionBuilder().term(variable).build()
        self.assertEqual(expression.get_value_name('x'), variable.value)

    def testGivenExpressionWithTwoVariablesWithSameNameWhenGetValueNameThenNotSimplifiedIsRaised(self):
        variable = VariableBuilder().name('x').build()
        expression = ExpressionBuilder().term(variable).term(variable.clon()).build()
        self.assertRaises(NotSimplified, expression.get_value_name, 'x')

    def testGivenExpressionWithVariableAndConstantWhenGetValueNameThenVariableValueIsReturned(self):
        variable = VariableBuilder().name('x').build()
        expression = ExpressionBuilder().default_constant().term(variable).build()
        self.assertEqual(expression.get_value_name('x'), variable.value)

    def testGivenExpressionTwoWithVariablesWithDifferentNamesWhenGetValueNameThenCorrectVariableValueIsReturned(self):
        variable = VariableBuilder().name('x').build()
        expression = ExpressionBuilder().term(VariableBuilder().name('y').build()).term(variable).build()
        self.assertEqual(expression.get_value_name('x'), variable.value)

    def testGivenExpressionWithVariablesWithSpecificNamesWhenGetValueNameWithOtherVariableNameThenLookupErrorIsRaised(
            self):
        expression = ExpressionBuilder().term(VariableBuilder().name('y').build()).term(
            VariableBuilder().name('z').build()).default_constant().build()
        self.assertRaises(LookupError, expression.get_value_name, 'x')

    # apply tests
    def testGivenExpressionWithVariableWhenApplyThenGetValueReturnsCorrectValue(self):
        expression = ExpressionBuilder().term(VariableBuilder().name('x').value(3.0).build()).build()
        expression.apply('x', 1.0)
        self.assertEqual(expression.get_value(), 3.0)

    def testGivenExpressionWithTwoVariablesWithSameNameWhenApplyAndSimplifyThenGetValueReturnsCorrectValue(self):
        expression = ExpressionBuilder().term(VariableBuilder().name('x').value(3.0).build()). \
            term(VariableBuilder().name('x').value(2.0).build()).build()
        expression.apply('x', 1.0)
        expression.simplify()
        self.assertEqual(expression.get_value(), 5.0)

    def testGivenExpressionWithVariableWhenApplyWrongValueThenGetValueRaisesLookupError(self):
        expression = ExpressionBuilder().term(VariableBuilder().name('x').build()).build()
        expression.apply('y', 1.0)
        self.assertRaises(LookupError, expression.get_value)

    # has_name tests
    def testGivenEmptyExpressionWhenHasNameThenReturnsFalse(self):
        expression = ExpressionBuilder().build()
        self.assertFalse(expression.has_name('x'))

    def testGivenExpressionWithConstantOnlyWhenHasNameThenReturnsFalse(self):
        expression = ExpressionBuilder().default_constant().build()
        self.assertFalse(expression.has_name('x'))

    def testGivenExpressionWithVariableOnlyWhenHasNameWithVariableNameThenReturnsTrue(self):
        variable = VariableBuilder().build()
        expression = ExpressionBuilder().term(variable).build()
        self.assertTrue(expression.has_name(variable.name))

    def testGivenExpressionWithVariableOnlyWhenHasNameWithDifferentVariableNameThenReturnsFalse(self):
        variable = VariableBuilder().name('x').build()
        expression = ExpressionBuilder().term(variable).build()
        self.assertFalse(expression.has_name('y'))

    def testGivenExpressionWithTwoVariablesWithDifferentNamesWhenHasNameWithVariableNameThenReturnsTrue(self):
        variable = VariableBuilder().name('x').build()
        expression = ExpressionBuilder().term(variable).term(VariableBuilder().name('y').build()).build()
        self.assertTrue(expression.has_name(variable.name))

    # get_name_set tests
    def testGivenEmptyExpressionWhenGetNameSetThenEmptySetIsReturned(self):
        expression = ExpressionBuilder().build()
        self.assertEqual(expression.get_name_set(), set())

    def testGivenExpressionWithConstantOnlyWhenGetNameSetThenEmptySetIsReturned(self):
        expression = ExpressionBuilder().default_constant().build()
        self.assertEqual(expression.get_name_set(), set())

    def testGivenExpressionWithOneVariableOnlyWhenGetNameSetThenSetWithVariableNameIsReturned(self):
        variable = VariableBuilder().name('x').build()
        expression = ExpressionBuilder().term(variable).build()
        self.assertEqual(expression.get_name_set(), {variable.name})

    def testGivenExpressionWithTwoVariablesWithSameNameWhenGetNameSetThenSetWithVariablesNameIsReturned(self):
        variable = VariableBuilder().name('x').build()
        expression = ExpressionBuilder().term(variable).term(variable.clon()).build()
        self.assertEqual(expression.get_name_set(), {variable.name})

    def testGivenExpressionWithTwoVariablesWithDifferentNameWhenGetNameSetThenSetWithVariablesNamesIsReturned(self):
        variable1 = VariableBuilder().name('x').build()
        variable2 = VariableBuilder().name('y').build()
        expression = ExpressionBuilder().term(variable1).term(variable2).build()
        self.assertEqual(expression.get_name_set(), {variable1.name, variable2.name})

    # equal tests
    def testGivenTwoEmptyExpressionsWhenEqualThenReturnsTrue(self):
        self.assertTrue(ExpressionBuilder().build().equal(ExpressionBuilder().build()))

    def testGivenTwoExpressionsWithDefaultConstantWhenEqualThenReturnsTrue(self):
        self.assertTrue(ExpressionBuilder().default_constant().build().equal(
            ExpressionBuilder().default_constant().build()))

    def testGivenTwoExpressionsWithDifferentConstantTermsThatSumTheSameValueWhenEqualThenReturnsFalse(self):
        constant = ConstantBuilder().build()
        double_constant = constant.clon()
        double_constant.multiply(2.0)
        self.assertFalse(ExpressionBuilder().term(double_constant).build().equal(
            ExpressionBuilder().term(constant).term(constant).build()))

    def testGivenTwoExpressionsWithSameTermsInDifferentOrderWhenEqualThenReturnsTrue(self):
        self.assertTrue(ExpressionBuilder().default_constant().default_variable().build().equal(
            ExpressionBuilder().default_variable().default_constant().build()))

    # clon tests
    def testGivenNotEmptyExpressionWhenClonThenExpressionEqualsReturnsTrue(self):
        expression = ExpressionBuilder().default_constant().default_variable().default_variable().build()
        expression_clon = expression.clon()
        self.assertFalse(expression is expression_clon)
        self.assertTrue(expression.equal(expression_clon))

    # add_expression tests
    def testGivenEmptyExpressionWhenAddExpressionThenEqualsReturnsTrue(self):
        expression1 = ExpressionBuilder().build()
        expression2 = ExpressionBuilder().default_constant().default_variable().build()
        expression1.add_expression(expression2)
        self.assertTrue(expression1.equal(expression2))

    def testGivenExpressionWithOneVariableWhenAddExpressionWithOtherVariableAndConstantThenExpressionContainsAllTerms(
            self):
        variable1 = VariableBuilder().name('x').build()
        variable2 = VariableBuilder().name('y').build()
        constant = ConstantBuilder().value(1.0).build()
        expression1 = ExpressionBuilder().term(variable1).build()
        expression2 = ExpressionBuilder().term(variable2).term(constant).build()
        expression1.add_expression(expression2)
        self.assertEqual(expression1.get_name_set(), {variable1.name, variable2.name})
        self.assertEqual(expression1.get_value(), constant.value)

    def testGivenTwoExpressionsWithConstantsWhenAddExpressionThenExpressionDoesNotSimplify(
            self):
        expression = ExpressionBuilder().default_constant().build()
        expression.add_expression(expression.clon())
        self.assertRaises(NotSimplified, expression.get_value)

    # multiply tests
    def testGivenExpressionWithConstantAndVariableWhenMultiplyThenGetValuesReturnsMultipliedTermsValues(self):
        constant = ConstantBuilder().build()
        variable = VariableBuilder().build()
        expression = ExpressionBuilder().term(constant).term(variable).build()
        multiply_value = 2.0
        expression.multiply(multiply_value)
        constant.multiply(multiply_value)
        variable.multiply(multiply_value)
        self.assertEqual(expression.get_value(), constant.value)
        self.assertEqual(expression.get_value_name(variable.name), variable.value)

    # simplify tests
    def testGivenExpressionWithOneConstantWhenSimplifyThenSameExpressionIsObtained(self):
        expression = ExpressionBuilder().default_constant().build()
        expression2 = expression.clon()
        expression.simplify()
        self.assertTrue(expression.equal(expression2))

    def testGivenEmpyExpressionWhenSimplifyThenEmptyExpressionIsObtained(self):
        expression = ExpressionBuilder().build()
        expression.simplify()
        self.assertTrue(expression.empty())

    def testGivenExpressionWithTwoConstantsWhenSimplifyThenExpressionWithOneConstantWithCorrectValueIsObtained(self):
        constant1 = ConstantBuilder().build()
        expression = ExpressionBuilder().term(constant1).term(constant1).build()
        expression.simplify()
        self.assertTrue(expression.get_value(), 2 * constant1.value)

    def testGivenExpressionWithTwoConstantsWithInverseValuesWhenSimplifyThenExpressionWithConstantWithValue0IsObtained(
            self):
        constant1 = ConstantBuilder().build()
        constant2 = constant1.clon()
        constant2.multiply(-1.0)
        expression = ExpressionBuilder().term(constant1).term(constant2).build()
        expression.simplify()
        self.assertEqual(expression.get_value(), 0.0)

    # simplify_name tests
    def testGivenExpressionWithOneVariableWhenSimplifyNameThenSameExpressionIsObtained(self):
        variable = VariableBuilder().build()
        expression = ExpressionBuilder().term(variable).build()
        expression2 = expression.clon()
        expression.simplify_name(variable.name)
        self.assertTrue(expression.equal(expression2))

    def testGivenEmpyExpressionWhenSimplifyNameThenEmptyExpressionIsObtained(self):
        expression = ExpressionBuilder().build()
        expression.simplify_name('any_name')
        self.assertTrue(expression.empty())

    def testGivenExpressionWithTwoVariablesSameNameWhenSimplifyThenExpressionWithOneVariableWithCorrectValueIsObtained(
            self):
        variable1 = VariableBuilder().name('x').build()
        expression = ExpressionBuilder().term(variable1).term(variable1).term(
            VariableBuilder().name('y').build()).default_constant().build()
        expression.simplify_name(variable1.name)
        self.assertTrue(expression.get_value_name(variable1.name), 2 * variable1.value)

    def testGivenExpressionWithTwoVariablesWithInverseValuesWhenSimplifyThenExpressionWithNoVariablesAndConstantWithValue0IsObtained(
            self):
        variable1 = VariableBuilder().build()
        variable2 = variable1.clon()
        variable2.multiply(-1.0)
        expression = ExpressionBuilder().term(variable1).term(variable2).build()
        expression.simplify_name(variable1.name)
        self.assertEqual(expression.get_value(), 0.0)
        self.assertRaises(LookupError, expression.get_value_name, variable1.name)
