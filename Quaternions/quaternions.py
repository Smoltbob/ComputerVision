import numpy as np

# todo: SO2, complex


class Quaternion:
    def __init__(self, coeffs: list):
        # q = a + bi + cj + dk
        self.w = coeffs

    def __repr__(self):
        return f"q = {self.a} + {self.b}i + {self.c}j + {self.d}k"

    def scalar(self):
        return self.w[0]

    def vector(self):
        return self.w[1:]

    def isScalar(self):
        return sum(self.vector()) == 0  # TODO proper floating point

    def isVector(self):
        return sum(self.scalar()) == 0
