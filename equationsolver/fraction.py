from copy import deepcopy


class Fraction:
    def __init__(self, num, den):
        if isinstance(num, Fraction):
            raise ValueError
        if isinstance(den, Fraction):
            raise ValueError
        self._num = num
        self._den = den

    def __float__(self):
        return float(self._num) / self._den

    def __int__(self):
        return int(float(self))

    def __mul__(self, other):
        temp = deepcopy(self)
        temp *= other
        return temp

    def __add__(self, other):
        temp = deepcopy(self)
        temp += other
        return temp

    def __div__(self, other):
        temp = deepcopy(self)
        temp /= other
        return temp

    def __sub__(self, other):
        temp = deepcopy(self)
        temp -= other
        return temp

    def __imul__(self, other):
        if isinstance(other, Fraction):
            self.multiply_fraction(other)
        else:
            self.multiply_value(other)
        return self

    def __iadd__(self, other):
        if isinstance(other, Fraction):
            self.add_fraction(other)
        else:
            self.add_fraction(Fraction(other, 1))
        return self

    def __idiv__(self, other):
        if isinstance(other, Fraction):
            self.divide_fraction(other)
        else:
            self.divide_value(other)
        return self

    def __isub__(self, other):
        self.__iadd__(other * -1)
        return self

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return (self * -1) + other

    def __rmul__(self, other):
        return self * other

    def __rdiv__(self, other):
        if isinstance(other, Fraction):
            return other / self
        else:
            return Fraction(other, 1) / self

    def __abs__(self):
        return Fraction(abs(self._num), abs(self._den))

    def __neg__(self):
        return Fraction(-self._num, self._den)

    def __eq__(self, other):
        if isinstance(other, Fraction):
            return self._num == other._num and self._den == other._den
        else:
            return self._num/self._den == other

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __ge__(self, other):
        return float(self) >= float(other)

    def __le__(self, other):
        return float(self) <= float(other)

    def __lt__(self, other):
        return self <= other and self != other

    def __gt__(self, other):
        return self >= other and self != other

    def add_fraction(self, other):
        self._num = self._num * other._den + other._num * self._den
        self._den = self._den * other._den
        self._simplify()

    def multiply_value(self, value):
        self.multiply_fraction(Fraction(value, 1))

    def multiply_fraction(self, fraction):
        self._num *= fraction._num
        self._den *= fraction._den
        self._simplify()

    def divide_value(self, value):
        self.multiply_fraction(Fraction(1, value))

    def divide_fraction(self, fraction):
        self.multiply_fraction(Fraction(fraction._den, fraction._num))

    def _simplify(self):
        a = abs(self._num)
        b = abs(self._den)
        if a != 0 and b > 1:
            while b != 0:
                if a > b:
                    a -= b
                else:
                    b -= a
            self._num /= a
            self._den /= a
        if self._den < 0:
            self._den = abs(self._den)
            self._num *= -1

    def __repr__(self):
        return 'Fraction(' + str(self._num) + ', ' + str(self._den) + ')'

    def __str__(self):
        if self._den != 1:
            return str(self._num) + '/' + str(self._den)
        else:
            return str(self._num)
