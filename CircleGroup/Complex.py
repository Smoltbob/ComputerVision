from math import sqrt, atan2

class Complex:
    def __init__(self, real, imag):
        # TODO polar form
        self.r = real
        self.i = imag

    def __eq__(self, rhs):
        self.r == rhs.r and self.i == rhs.i

    def conjugate(self):
        return Complex(self.r, -self.i)

    def _add__(self, rhs):
        return Complex(self.r + rhs.r, self.i + rhs.i)

    def __sub__(self, rhs): 
        return Complex(self.r - rhs.r, self.i - rhs.i)

    def __mul__(self, rhs):
        return Complex(self.r * rhs.r - self.i * rhs.i, self.r * rhs.i + self.i * rhs.r)

    def inverse(self):
        return Complex(self.r / (self.r ** 2 + self.i ** 2), -self.i / (self.r ** 2 + self.i ** 2))

    def __div__(self, rhs):
        # TODO check rhs non zero
        den = rhs.r ** 2 + rhs.i ** 2
        return Complex((self.r * rhs.r + self.i * rhs.i)/den, (self.r * rhs.i - self.i * rhs.r)/den)
        
    def magnitude(self):
        # TODO use squared norm from math utils
        return sqrt(self.r ** 2 + self.i ** 2)

    def angle(self):
        return atan2(self.i, self.r)