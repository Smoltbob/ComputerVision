from lib.Math.math_utils import cos, sin

def make_2d_rot_mat(angle):
    # angle in radians
    return [
        [cos(angle), -sin(angle)],
        [sin(angle), cos(angle)]
    ]