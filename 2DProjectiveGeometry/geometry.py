"""
Note: this is the Euclidian version of the Inner product
"""
def dot(vecA, vecB):
    assert(len(vecA) == len(vecB))

    total = 0
    for a, b in zip(vecA, vecB):
        total += a * b
    return total

"""
Note this is the 3D version of the exterior product = wedge operator
"""
def cross(vecA, vecB):
    a = vecA[1] * vecB[2] - vecA[2] * vecB[1]
    b = vecA[2] * vecB[0] - vecA[0] * vecB[2]
    c = vecA[0] * vecB[1] - vecA[1] * vecB[0]
    return [a, b, c]
