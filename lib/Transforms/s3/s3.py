from lib.Math.Quaternions.quaternions import Quaternion
from lib.Math.math_utils import normalize


class S3(Quaternion):
    def __init__(self, coeffs):
        super().__init__(coeffs)

        if self.norm() != 1:
            self.w = normalize(self.w)

    def __matmul__(self, rhs):
        # The hamilton product is inherited from Quaternion
        return S3(super().__matmul__(rhs).w)

    def from_matrix(R):
        # see https://d3cw3dd2w32x2b.cloudfront.net/wp-content/uploads/2015/01/matrix-to-quat.pdf
        # TODO refactor the representation convertions into separate file ?
        r00 = R[0][0]
        r01 = R[0][1]
        r02 = R[0][2]
        r10 = R[1][0]
        r11 = R[1][1]
        r12 = R[1][2]
        r20 = R[2][0]
        r21 = R[2][1]
        r22 = R[2][2]

        if r22 < 0:
            if r00 > r11:
                vx = 1 + r00 - r11 - r22
                vy = r10 + r01
                vz = r02 + r20
                sw = r21 - r12

            else:
                vx = r10 + r01
                vy = 1 - r00 + r11 - r22
                vz = r21 + r12
                sw = r02 - r20

        else:
            if r00 < -r11:
                vx = r02 + r20
                vy = r21 + r12
                vz = 1 - r00 - r11 + r22
                sw = r10 - r01

            else:
                vx = r21 - r12
                vy = r02 - r20
                vz = r10 - r01
                sw = 1 + r00 + r11 + r22

        coeffs = [sw, vx, vy, vz]
        return S3(normalize(coeffs))

    def to_matrix(self):
        qr, qi, qj, qk = self.w
        r00 = 1 - 2 * (qj**2 + qk**2)
        r01 = 2 * (qi * qj - qk * qr)
        r02 = 2 * (qi * qk + qj * qr)
        r10 = 2 * (qi * qj + qk * qr)
        r11 = 1 - 2 * (qi**2 + qk**2)
        r12 = 2 * (qj * qk - qi * qr)
        r20 = 2 * (qi * qk - qj * qr)
        r21 = 2 * (qj * qk + qi * qr)
        r22 = 1 - 2 * (qi**2 + qj**2)

        return [[r00, r01, r02], [r10, r11, r12], [r20, r21, r22]]

    def log_map(self, numerically_stable=False):
        # Ie from Quaternion to axis angle
        # See https://vision.in.tum.de/_media/members/demmeln/nurlanov2021so3log.pdf
        if numerically_stable:
            return

        factor = 2 * acos(self.scalar())
        return [factor * x for x in normalize(self.vector())]

    def from_algebra(w):
        # ie from_axis angle, ie exp_map
        if sum([x for x in w]) == 0:
            return S3([1, 0, 0, 0])

        angle = norm(w) / 2
        scalar = cos(angle)
        vector_factor = sin(angle) / norm(w)
        return S3([scalar, *[vector_factor * x for x in w]])
