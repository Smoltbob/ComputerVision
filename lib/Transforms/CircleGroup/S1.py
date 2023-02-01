from lib.Transforms.CircleGroup.Complex import *
from lib.Math.math_utils import cos, sin
from lib.Math.constants import pi

class S1:
    def __init__(self, angle = 0):
        """
        TODO enforce unit complex
        Note angle is in radians, defined counter clockwise
        around the origin.
        """
        self.z = Complex(cos(angle), sin(angle))
        assert(self.z.magnitude() - 1 < 1e-9) # TODO floating point

    def __repr__(self):
        return f"S1: {self.log_map()} rads"

    def __matmul__(self, rhs):
        tmp = S1()
        tmp.z = self.z * rhs.z
        assert(tmp.z.magnitude() - 1 < 1e-9)
        return tmp

    def angle(self):
        return self.z.angle()

    def inverse(self):
        # TODO constructor from z / build S1 with -angle
        tmp = S1()
        tmp.z = self.z.inverse()
        assert(tmp.z.magnitude() - 1 < 1e-9)
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

    def distance_from(self, rhs: "S1"):
        """
        Returns the signed distance between two angles,
        ie a value in (-pi, pi] that is the minimum angular displacement
        from rhs to self.
        """
        theta1 = self.angle()
        theta2 = rhs.angle()

        diff_t2_t1 = theta2 - theta1

        if diff_t2_t1 > -pi and diff_t2_t1 <= pi:
            return diff_t2_t1
        elif diff_t2_t1 > pi:
            return diff_t2_t1 - 2 *pi
        else: # diff_t2_t1 <= -pi
            return diff_t2_t1 + 2*pi

    def geodesic_ditance(self, rhs):
        return abs(self.distance_from(rhs))