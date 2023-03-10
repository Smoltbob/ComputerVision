from lib.Math.Quaternions.quaternions import Quaternion
from lib.Math.math_utils import normalize, acos, sin, norm, cos


"""
A Unit Quaternion is a Quaternion that is initiliazed with unit norm.
It supports the same operations as Quaternions.
It may loose its identity and thus operations on Unit Quaternions must take
care of this.
"""


class S3(Quaternion):
    def __init__(self, coeffs):
        super().__init__(coeffs)

        if self.norm() != 1:
            self.w = normalize(self.w)

    def from_algebra(w):
        # ie from_axis angle, ie exp_map
        if sum([x for x in w]) == 0:
            return S3([1, 0, 0, 0])

        angle = norm(w) / 2
        scalar = cos(angle)
        vector_factor = sin(angle) / norm(w)
        return S3([scalar, *[vector_factor * x for x in w]])
