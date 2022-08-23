import sys

sys.path.append("../Complex")
from Complex import *
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

    def norm(self):
        pass

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
        return self.z.angle()
