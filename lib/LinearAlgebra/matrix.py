
from numpy.linalg import svd

def transpose(matrix):
    # Prerequisite: square matrix
    assert(len(matrix) > 2, f"Cannot transpose matrix with {len(matrix)} rows")
    for row in matrix:
        assert(len(row) == len(matrix), "Cannot transpose non-square matrix")
        
    newmatrix = []
    for i in range(len(matrix)):
        newrow = []
        for j in range(0, len(row)):
            newrow.append(matrix[j][i])
        newmatrix.append(newrow)

    return newmatrix


def compute_determinant_3x3(matrix):
    # Prerequisite: 3x3 matrix
    assert(len(matrix) == 3, "Cannot compute determinant of non 3x3 matrix")
    for row in matrix:
        assert(len(row) == 3, "Cannot compute determinant of non 3x3 matrix")
    
    a, b, c = row[0]
    d, e, f = row[1]
    g, h, i = row[2]

    return a*e*i + b*f*g + c*d*h - c*e*g - b*d*i - a*f*h


def matrix_rank(matrix, threshold = 1e-9):
    singular_values = svd(matrix, compute_uv=False)
    return sum(singular_values > threshold)