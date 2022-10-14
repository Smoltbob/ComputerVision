import sys
sys.path.append("../2DProjectiveGeometry")
from math_utils import cos, sin

def generate_spiral(coils, radius):
    """
    Generate an Archimedean spiral
    - thetaMax: value of theta for the last coil, 
    ie how many radiants we need to rotate in total.
    - awayStep: how much to move away from the center 
    at each step
    - chord = distance between points
    - theta = outwards angle for each next point
    Algorithm from https://stackoverflow.com/questions/13894715/draw-equidistant-points-on-a-spiral
    """
    thetaMax = coils * 2 * 3.1415
    awayStep = radius / thetaMax
    chord = 1

    points_set = [[0, 0]]
    theta = chord / awayStep
    while theta < thetaMax:
        away = awayStep * theta
    
        # Polar to cartesian
        x = cos(theta) * away
        y = sin(theta) * away

        points_set.append([x, y])
        theta += chord / away

    return points_set