import numpy as np
from lib.Math.quaternions import *
from lib.Math.constants import pi
from lib.Math.math_utils import sqrt, atan2, acos, cos, sin, norm
from lib.LinearAlgebra.matrix import transpose, compute_determinant_3x3, trace


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

    def inverse(self):
        return SO3(transpose(self.R))

    def rotation_axis(self):
        assert self.isValid(self.R), "Rotation is invalid"
        rotation_matrix = self.R

        rotation_trace = trace(rotation_matrix)

        if rotation_trace >= 3:
            # we have a unit rotation
            return [0, 0, 0]

        rotation_matrix = np.array(rotation_matrix)

        S = (
            rotation_matrix
            + rotation_matrix.T
            - (rotation_trace - 1) * np.eye(3)
        )
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
            -rot_matrix[2, 0],
            sqrt(rot_matrix[2, 1] ** 2 + rot_matrix[2, 2] ** 2),
        )
        roll = atan2(rot_matrix[2, 1], rot_matrix[2, 2])

        if units == "deg":
            rad_2_deg = 180 / pi
            return rad_2_deg * yaw, rad_2_deg * pitch, rad_2_deg * roll
        return yaw, pitch, roll

    def angle(self):
        return acos((np.trace(self.R) - 1) / 2)

    """
    def centered_log_map(self, other):

    Returns the log map centered on other
   
    centered_SO3 = SO3(self.R @ other.R.T)  # R@S^-1
    return centered_SO3.log_map()
    """

    @staticmethod
    def isValid(rotation):
        # Checks that the rotation matrix is valid
        kDetTrhreshold = 1e-6
        determinant_is_one = (
            abs(compute_determinant_3x3(rotation) - 1) < kDetTrhreshold
        )
        is_orthonormal = np.allclose(
            np.array(rotation) @ np.array(transpose(rotation)), np.eye(3)
        )

        return determinant_is_one and is_orthonormal
