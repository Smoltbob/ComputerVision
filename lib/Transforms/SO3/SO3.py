import numpy as np
from lib.Math.Quaternions.quaternions import *
from lib.Math.constants import pi
from lib.Math.math_utils import sqrt, atan2, cos, sin


def skew(v):
    return [[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]


def vee(W):
    return [-W[1][2], W[0][2], -W[0][1]]


class SO3:
    def __init__(self, R=None):
        if R is None:
            R = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.R = R

    def __repr__(self):
        return f"SO3: {self.R}"

    def __matmul__(self, rhs):
        # TODO check that they both have the same type and representation
        return SO3(self.R @ rhs.R)

    def ypr(self, units="deg"):
        rot_matrix = self.R
        yaw = atan2(rot_matrix[1, 0], rot_matrix[0, 0])
        pitch = atan2(
            -rot_matrix[2, 0], sqrt(rot_matrix[2, 1] ** 2 + rot_matrix[2, 2] ** 2)
        )
        roll = atan2(rot_matrix[2, 1], rot_matrix[2, 2])

        if units == "deg":
            rad_2_deg = 180 / pi
            return rad_2_deg * yaw, rad_2_deg * pitch, rad_2_deg * roll
        return yaw, pitch, roll

    def log_map(self):
        """
        Returns the skew matrix in lie algebra associated to the
        SO3 rotation matrix R
        """
        R = self.R
        A = (R - R.T) / 2
        norm = sqrt(-np.trace(A @ A) / 2)
        skew_matrix = ((np.arcsin(norm)) / norm) * A
        return so3(vee(skew_matrix))

    def centered_log_map(self, other):
        """
        Returns the log map centered on other
        """
        centered_SO3 = SO3(self.R @ other.R.T)  # R@S^-1
        return centered_SO3.log_map()


class so3:
    def __init__(self, w):
        self.w = w  # euler angles

    def __repr__(self):
        return f"so3: {self.w}"

    def exp_map_generic(self):
        """
        Simply computes the matrix exponent.
        We should iterate to infinity but we stop at 50.
        """
        A = skew(self.w)
        exp = np.eye(3)
        for k in range(1, 50):
            exp += (1 / np.math.factorial(k)) * np.linalg.matrix_power(A, k)
        return SO3(exp)

    def exp_map_euler(self):
        """
        SO3 specific implementation
        """
        w = np.array(self.w)
        theta = np.linalg.norm(w)
        w = w / theta
        x = w[0]
        y = w[1]
        z = w[2]

        c = cos(theta / 2)
        s = sin(theta / 2)

        exp = [
            [
                2 * (x**2 - 1) * s**2 + 1,
                2 * x * y * (s**2) - 2 * z * c * s,
                2 * x * z * s**2 + 2 * y * c * s,
            ],
            [
                2 * x * y * s**2 + 2 * z * c * s,
                2 * (y**2 - 1) * s**2 + 1,
                2 * y * z * s**2 - 2 * x * c * s,
            ],
            [
                2 * x * z * s**2 - 2 * y * c * s,
                2 * y * z * s**2 + 2 * x * c * s,
                2 * (z**2 - 1) * s**2 + 1,
            ],
        ]
        return SO3(np.array(exp))
