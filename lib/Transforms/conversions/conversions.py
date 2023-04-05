from lib.Transforms.s3.s3 import S3
from lib.Transforms.SO3.SO3 import SO3
from lib.Transforms.so3.so3 import so3
from lib.Math.math_utils import sin, acos, cos, norm, sqrt
import numpy as np


def skew(v):
    return [[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]


def vee(W):
    return [-W[1][2], W[0][2], -W[0][1]]


def S3_from_SO3(SO3):
    """
    Matrix to unit quaternion conversion
    see https://d3cw3dd2w32x2b.cloudfront.net/wp-content/uploads/2015/01/matrix-to-quat.pdf
    """
    SO3_matrix = SO3.R

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

    w, x, y, z = S3_quat.w

    txx = 2 * x * x
    tyy = 2 * y * y
    tzz = 2 * z * z
    tzz = 2 * z * z
    txy = 2 * x * y
    txz = 2 * x * z
    tyz = 2 * y * z
    txw = 2 * x * w
    tyw = 2 * y * w
    tzw = 2 * z * w

    R = [
        [1 - (tyy + tzz), (txy - tzw), (txz + tyw)],
        [(txy + tzw), 1 - (txx + tzz), (tyz - txw)],
        [(txz - tyw), (tyz + txw), 1 - (txx + tyy)],
    ]

    return SO3(R)


def SO3_to_log(SO3_mat):
    """
    Log map, from rotation matrix to tangent space

    Returns the skew matrix in lie algebra associated to the
    SO3 rotation matrix R
    """
    R = SO3_mat.R
    angle = SO3_mat.angle()
    rotation_log = (angle / (2 * sin(angle))) * (np.array(R) - np.array(R).T)

    return so3(vee(rotation_log))


def log_to_SO3(so3):
    """
    SO3 specific implementation
    """
    w = np.array(so3.w)
    angle = so3.angle()
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


def S3_to_log(S3_quat):
    # Ie from Quaternion to axis angle
    # See https://vision.in.tum.de/_media/members/demmeln/nurlanov2021so3log.pdf
    # https://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToAngle/index.htm

    angle = 2 * acos(S3_quat.scalar())
    axis = [x / sqrt(1 - S3_quat.scalar() ** 2) for x in S3_quat.vector()]
    return so3([angle * x for x in axis])


def log_to_S3(so3):
    w = so3.w
    # ie from_axis angle, ie exp_map
    if sum([x for x in w]) == 0:
        return S3([1, 0, 0, 0])

    angle = norm(w) / 2
    scalar = cos(angle)
    vector_factor = sin(angle) / norm(w)
    return S3([scalar, *[vector_factor * x for x in w]])
