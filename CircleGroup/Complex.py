class Complex:
    def __init__(self, real, imag):
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

    def __div__(self, rhs):
        # TODO check rhs non zero
        den = rhs.r ** 2 + rhs.i ** 2
        return Complex((self.r * rhs.r + self.i * rhs.i)/den, (self.r * rhs.i - self.i * rhs.r)/den)
        