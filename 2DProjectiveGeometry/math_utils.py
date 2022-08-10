from math import sqrt


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
