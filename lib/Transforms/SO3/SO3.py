import numpy as np
from lib.Math.Quaternions.quaternions import *
from lib.Math.constants import pi
from lib.Math.math_utils import sqrt, atan2, acos, cos, sin, norm
from lib.LinearAlgebra.matrix import transpose, compute_determinant_3x3, trace


def skew(v):
    return [[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]


def vee(W):
    return [-W[1][2], W[0][2], -W[0][1]]


# TODO consider refactoring to using class methods instead
class SO3:
    def __init__(self, R=None):
        if R is None:
            R = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

        assert self.isValid(R), "Rotation is invalid"
        self.R = R

    def __repr__(self):
        return f"SO3: {self.R}"

    def __matmul__(self, rhs):
        # TODO check that they both have the same type and representation
        return SO3(self.R @ rhs.R)

    def rotation_axis(self):
        assert self.isValid(self.R), "Rotation is invalid"
        rotation_matrix = self.R

        rotation_trace = trace(rotation_matrix)

        if rotation_trace >= 3:
            # we have a unit rotation
            return [0, 0, 0]

        rotation_matrix = np.array(rotation_matrix)

        S = rotation_matrix + rotation_matrix.T - (rotation_trace - 1) * np.eye(3)
        c = 1 / (3 - rotation_trace)

        n = [0, 0, 0]
        for i in range(3):
            if S[i][i] > 0:
                n[i] = sqrt(S[i][i] * c)

        if n[0] > 0:
            if S[1][0] < 0:
                n[1] *= -1
            if S[2][0] < 0:
                n[2] *= -1
        elif S[2][1] < 0:
            n[1] *= -1

        return n

    # TODO move to Transforms/conversions
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

    def angle(self):
        return acos((np.trace(self.R) - 1) / 2)

    def log_map(self):
        """
        Returns the skew matrix in lie algebra associated to the
        SO3 rotation matrix R
        """
        R = self.R
        angle = self.angle()
        rotation_log = (angle / (2 * sin(angle))) * (np.array(R) - np.array(R).T)
        return so3(vee(rotation_log))

    def centered_log_map(self, other):
        """
        Returns the log map centered on other
        """
        centered_SO3 = SO3(self.R @ other.R.T)  # R@S^-1
        return centered_SO3.log_map()

    @classmethod
    def SO3_median(rotation_list: list, threshold=1e-6, S_t=None):
        # We provide S_t as a first guess
        assert S_t is not None

        for _ in range(100):
            elements = np.array([x.centered_log_map(S_t).w for x in rotation_list])
            numerator = 0
            denumerator = 0
            for xi in elements:
                X = np.linalg.norm(xi)
                numerator += xi / X
                denumerator += 1 / X
            delta = numerator / denumerator
            S_t = SO3.so3(delta).exp_map_euler() @ S_t

            if np.linalg.norm(delta) < threshold:
                break

        return S_t

    @classmethod
    def SO3_mean(rotations):
        # Correct ?
        v_is = np.array([x.log_map().w for x in rotations])
        return SO3.so3(np.mean(v_is, axis=0)).exp_map_euler()

    @staticmethod
    def isValid(rotation):
        # Checks that the rotation matrix is valid
        kDetTrhreshold = 1e-6
        determinant_is_one = abs(compute_determinant_3x3(rotation) - 1) < kDetTrhreshold
        is_orthonormal = np.allclose(rotation, transpose(rotation))

        return determinant_is_one and is_orthonormal


class so3:
    def __init__(self, w):
        self.w = w  # euler angles

    def __repr__(self):
        return f"so3: {self.w}"

    def angle(self):
        return norm(self.w)

    def exp_map_euler(self):
        """
        SO3 specific implementation
        """
        w = np.array(self.w)
        angle = self.angle()
        angle_squared = angle**2

        if angle_squared < 1e-6:
            a = 1 - (angle_squared / 6) * (1 - angle_squared / 20)
            b = 0.5 * (1 - angle_squared / 12)
        else:
            a = sin(angle) / angle
            b = (1 - cos(angle)) / angle_squared

        skew_matrix = skew(w)
        skew_matrix_squared = np.array(skew_matrix) @ np.array(skew_matrix)
        return SO3(np.eye(3) + a * np.array(skew_matrix) + b * skew_matrix_squared)
