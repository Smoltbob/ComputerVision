from lib.Math.quaternions import Quaternion
from lib.Math.math_utils import normalize


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
