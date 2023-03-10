from numpy.linalg import svd


"""
Utility matrix operations
"""


def transpose(matrix):
    # Prerequisite: square matrix
    assert len(matrix) > 2, f"Cannot transpose matrix with {len(matrix)} rows"
    for row in matrix:
        assert len(row) == len(matrix), "Cannot transpose non-square matrix"

    newmatrix = []
    for i in range(len(matrix)):
        newrow = []
        for j in range(0, len(row)):
            newrow.append(matrix[j][i])
        newmatrix.append(newrow)

    return newmatrix


def compute_determinant_3x3(matrix):
    # Prereqlen(matrix) == 3, "Cannot compute determinant of non 3x3 matrix")
    for row in matrix:
        assert len(row) == 3, "Cannot compute determinant of non 3x3 matrix"

    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]

    return (
        a * e * i + b * f * g + c * d * h - c * e * g - b * d * i - a * f * h
    )


def trace(matrix):
    # Prerequisite: square matrix
    assert len(matrix) > 2, f"Cannot transpose matrix with {len(matrix)} rows"
    for row in matrix:
        assert len(row) == len(matrix), "Cannot transpose non-square matrix"

    diag_sum = 0
    for i in range(len(matrix)):
        diag_sum += matrix[i][i]

    return diag_sum


def matrix_rank(matrix, threshold=1e-9):
    singular_values = svd(matrix, compute_uv=False)
    return sum(singular_values > threshold)
