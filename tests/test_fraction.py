import unittest

from equationsolver.fraction import Fraction


class FractionTestCase(unittest.TestCase):

    def testAddFractions(self):
        self.assertEqual(Fraction(2, 3), Fraction(1, 3) + Fraction(1, 3))
        self.assertEqual(Fraction(2, 3), Fraction(4, 3) - Fraction(2, 3))
        fraction = Fraction(1, 3)
        fraction += Fraction(1, 3)
        self.assertEqual(Fraction(2, 3), fraction)

    def testAddFractionNumber(self):
        self.assertEqual(Fraction(4, 3), Fraction(1, 3) + 1)
        self.assertEqual(Fraction(4, 3), 1 + Fraction(1, 3))
        self.assertEqual(Fraction(2, 3), 1 - Fraction(1, 3))
        self.assertEqual(Fraction(1, 3), Fraction(4, 3) - 1)
        fraction = Fraction(1, 3)
        fraction += 1
        self.assertEqual(Fraction(4, 3), fraction)
        fraction -= 1
        self.assertEqual(Fraction(1, 3), fraction)

    def testMultiplyNumber(self):
        self.assertEqual(Fraction(2, 3), Fraction(1, 3) * 2)
        self.assertEqual(Fraction(-2, 3), Fraction(1, 3) * (-2))
        self.assertEqual(Fraction(2, 3), 2 * Fraction(1, 3))
        self.assertEqual(Fraction(-2, 3), -2 * Fraction(1, 3))
        fraction = Fraction(1, 3)
        fraction *= 2
        self.assertEqual(Fraction(2, 3), fraction)

    def testMultiplyFractions(self):
        self.assertEqual(Fraction(2, 9), Fraction(1, 3) * Fraction(2, 3))
        fraction = Fraction(1, 3)
        fraction *= Fraction(2, 3)
        self.assertEqual(Fraction(2, 9), fraction)

    def testDivideNumber(self):
        self.assertEqual(Fraction(2, 3), Fraction(4, 3) / 2)
        self.assertEqual(Fraction(3, 1), 2 / Fraction(2, 3))
        fraction = Fraction(4, 3)
        fraction /= 2
        self.assertEqual(Fraction(2, 3), fraction)

    def testDivideFraction(self):
        self.assertEqual(Fraction(4, 9), Fraction(1, 3) / Fraction(3, 4))
        fraction = Fraction(1, 3)
        fraction /= Fraction(2, 3)
        self.assertEqual(Fraction(1, 2), fraction)
