from lib.Math.math_utils import norm, normalize, cos, sin, acos

# todo: SO2, complex


class Quaternion:
    def __init__(self, coeffs: list):
        # q = a + bi + cj + dk
        self.w = coeffs

    def __repr__(self):
        return f"q = {self.w[0]} + {self.w[1]}i + {self.w[2]}j + {self.w[3]}k"

    def scalar(self):
        return self.w[0]

    def vector(self):
        return self.w[1:]

    def isScalar(self):
        return sum(self.vector()) == 0  # TODO proper floating point

    def isVector(self):
        return self.scalar() == 0

    def angle(self):
        pass

    def __add__(self, rhs):
        """
        Component wise addition
        """
        return Quaternion(
            [
                self.w[0] + rhs.w[0],
                self.w[1] + rhs.w[1],
                self.w[2] + rhs.w[2],
                self.w[3] + rhs.w[3],
            ]
        )

    def __mul__(self, rhs: "scalar"):
        """
        Component wise multiplication by a scalar
        """
        # TODO type checking
        return Quaternion(
            [
                rhs * self.w[0],
                rhs * self.w[1],
                rhs * self.w[2],
                rhs * self.w[3],
            ]
        )

    def __matmul__(self, rhs):
        """
        Hamilton product
        """
        q1 = self.w
        q2 = rhs.w
        return Quaternion(
            [
                q1[0] * q2[0] - q1[1] * q2[1] - q1[2] * q2[2] - q1[3] * q2[3],
                q1[0] * q2[1] + q1[1] * q2[0] + q1[2] * q2[3] - q1[3] * q2[2],
                q1[0] * q2[2] - q1[1] * q2[3] + q1[2] * q2[0] + q1[3] * q2[1],
                q1[0] * q2[3] + q1[1] * q2[2] - q1[2] * q2[1] + q1[3] * q2[0],
            ]
        )

    def conjugate(self):
        return Quaternion([self.w[0], -self.w[1], -self.w[2], -self.w[3]])

    def inverse(self):
        assert sum(self.w) != 0  # TODO FP comparison
        factor = 1 / sum([x**2 for x in self.w])
        return self.conjugate() * factor

    def norm(self):
        return norm(self.w)


class UnitQuaternion(Quaternion):
    def __init__(self, coeffs):
        super().__init__(coeffs)

        if self.norm() != 1:
            self.w = normalize(self.w)

    def __matmul__(self, rhs):
        return UnitQuaternion(super().__matmul__(rhs).w)

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
        return UnitQuaternion(normalize(coeffs))

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
            return UnitQuaternion([1, 0, 0, 0])

        angle = norm(w) / 2
        scalar = cos(angle)
        vector_factor = sin(angle) / norm(w)
        return UnitQuaternion([scalar, *[vector_factor * x for x in w]])
