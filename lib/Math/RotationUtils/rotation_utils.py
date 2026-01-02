from lib.Math.math_utils import cos, sin
import numpy as np

def make_2d_rot_mat(angle):
    # angle in radians
    return [
        [cos(angle), -sin(angle)],
        [sin(angle), cos(angle)]
    ]

def euler_to_rot_mat(roll, pitch, yaw):
    """
    Typically yaw is z, pitch is y, roll is x
    Angles are in radians.
    """
    R_x = np.array([1, 0, 0,
            0, cos(roll), -sin(roll),
            0, sin(roll), cos(roll)])

    R_y = np.array([cos(pitch), 0, sin(pitch),
            0, 1, 0,
            -sin(pitch), 0, cos(pitch)])

    R_z = np.array([cos(yaw), -sin(yaw), 0,
            sin(yaw), cos(yaw), 0,
            0, 0, 1])

    # Combine the rotation matrices
    R = R_z.reshape(3, 3) @ R_y.reshape(3, 3) @ R_x.reshape(3, 3)

    return R