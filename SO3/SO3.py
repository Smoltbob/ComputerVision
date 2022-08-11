import numpy as np

import sys

sys.path.append("../Quaternions")
from quaternions import *


def skew(v):
    return [[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]


def vee(W):
    return [-W[1][2], W[0][2], -W[0][1]]


class SO3:
    def __init__(self, R=None):
        self.R = R

    def __repr__(self):
        return f"SO3: {self.R}"

    def __matmul__(self, rhs):
        # TODO check that they both have the same type and representation
        return SO3(q=self.R @ rhs.R)

    def log_map(self):
        """
        Returns the skew matrix in lie algebra associated to the
        SO3 rotation matrix R
        """
        R = self.R
        A = (R - R.T) / 2
        norm = np.sqrt(-np.trace(A @ A) / 2)
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

        c = np.cos(theta / 2)
        s = np.sin(theta / 2)

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
