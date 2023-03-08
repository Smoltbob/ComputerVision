from math import sqrt as _sqrt
from math import sin as _sin
from math import cos as _cos
from math import acos as _acos
from math import atan2 as _atan2
from math import exp as _exp
from math import log as _log


def dot(vecA, vecB):
    """
    Note: this is the Euclidian version of the Inner product
    """

    assert len(vecA) == len(vecB)

    total = 0
    for a, b in zip(vecA, vecB):
        total += a * b
    return total


def cross(vecA, vecB):
    """
    Note this is the 3D version of the exterior product = wedge operator
    """

    a = vecA[1] * vecB[2] - vecA[2] * vecB[1]
    b = vecA[2] * vecB[0] - vecA[0] * vecB[2]
    c = vecA[0] * vecB[1] - vecA[1] * vecB[0]
    return [a, b, c]


def squaredNorm(vec):
    return sum([x**2 for x in vec])


def norm(vec):
    return sqrt(squaredNorm(vec))


def normalize(vec):
    n = norm(vec)
    return [x / n for x in vec]


def sqrt(x):
    return _sqrt(x)


def atan2(x, y):
    return _atan2(x, y)


def sin(x):
    return _sin(x)


def cos(x):
    return _cos(x)


def acos(x):
    return _acos(x)


def exp(x):
    return _exp(x)


def log(x):
    return _log(x)


def absolute_value(vec):
    return [abs(x) for x in vec]
