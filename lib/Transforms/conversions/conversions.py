from lib.Transforms.s3.s3 import S3
from lib.Transforms.SO3 import SO3


def S3_from_SO3(SO3_matrix):
    """
    Matrix to unit quaternion conversion
    """
    # see https://d3cw3dd2w32x2b.cloudfront.net/wp-content/uploads/2015/01/matrix-to-quat.pdf
    r00 = SO3_matrix[0][0]
    r01 = SO3_matrix[0][1]
    r02 = SO3_matrix[0][2]
    r10 = SO3_matrix[1][0]
    r11 = SO3_matrix[1][1]
    r12 = SO3_matrix[1][2]
    r20 = SO3_matrix[2][0]
    r21 = SO3_matrix[2][1]
    r22 = SO3_matrix[2][2]

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
    return S3(coeffs)


def SO3_from_S3(S3_quat):
    """
    Unit quaternion to matrix conversion
    """
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

    R = [[r00, r01, r02], [r10, r11, r12], [r20, r21, r22]]
    return SO3(R)
