import sys

sys.path.append("../2DProjectiveGeometry")
from math_utils import norm

# todo: SO2, complex


class Quaternion:
    def __init__(self, coeffs: list):
        # q = a + bi + cj + dk
        self.w = coeffs

    def __repr__(self):
        return f"q = {self.w[0]} + {self.w[1]}i + {self.w[2]}j + {self.w[3]}k"

    def scalar(self):
        return self.w[0]

    def vector(self):
        return self.w[1:]

    def isScalar(self):
        return sum(self.vector()) == 0  # TODO proper floating point

    def isVector(self):
        return self.scalar() == 0

    def __add__(self, rhs):
        """
        Component wise addition
        """
        return Quaternion(
            [
                self.w[0] + rhs.w[0],
                self.w[1] + rhs.w[1],
                self.w[2] + rhs.w[2],
                self.w[3] + rhs.w[3],
            ]
        )

    def __mul__(self, rhs: "scalar"):
        """
        Component wise multiplication by a scalar
        """
        # TODO type checking
        return Quaternion(
            [
                rhs * self.w[0],
                rhs * self.w[1],
                rhs * self.w[2],
                rhs * self.w[3],
            ]
        )

    def __matmul__(self, rhs):
        """
        Hamilton product
        """
        q1 = self.w
        q2 = rhs.w
        return Quaternion(
            [
                q1[0] * q2[0] - q1[1] * q2[1] - q1[2] * q2[2] - q1[3] * q2[3],
                q1[0] * q2[1] + q1[1] * q2[0] + q1[2] * q2[3] - q1[3] * q2[2],
                q1[0] * q2[2] - q1[1] * q2[3] + q1[2] * q2[0] + q1[3] * q2[1],
                q1[0] * q2[3] + q1[1] * q2[2] - q1[2] * q2[1] + q1[3] * q2[0],
            ]
        )

    def conjugate(self):
        return Quaternion([self.w[0], -self.w[1], -self.w[2], -self.w[3]])

    def inverse(self):
        assert sum(self.w) != 0  # TODO FP comparison
        factor = 1 / sum([x**2 for x in self.w])
        return self.conjugate() * factor

    def norm(self):
        return norm(self.w)


class UnitQuaternion(Quaternion):
    pass
