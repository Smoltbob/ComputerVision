from lib.Transforms.CircleGroup.Complex import *
from math import cos, sin

class S1:
    def __init__(self, angle = 0):
        """
        TODO enforce unit complex
        Note angle is in radians, defined counter clockwise
        around the origin.
        """
        self.z = Complex(cos(angle), sin(angle))
        assert(self.z.magnitude() == 1) # TODO floating point

    def __repr__(self):
        return f"S1: {self.log_map()} rads"

    def __matmul__(self, rhs):
        tmp = S1()
        tmp.z = self.z * rhs.z
        return tmp

    def angle(self):
        return self.z.angle()

    def inverse(self):
        # TODO constructor from z / build S1 with -angle
        tmp = S1()
        tmp.z = self.z.inverse()
        return tmp

    def exp_map(rot_angle):
        """
        From angle in R to element in S1
        """
        return S1(rot_angle)

    def log_map(self):
        """
        From S1 to angle in R
        TODO enforce unity
        """
        return self.angle()

    def norm(self):
        return self.z.magnitude()
