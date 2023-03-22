import unittest
from lib.LinearAlgebra.matrix import transpose, compute_determinant_3x3
from random import random
import numpy as np


class TestMatrix(unittest.TestCase):
    def setUp(self):
        self.identity = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    def test_constructor(self):
        self.assertTrue(np.allclose(self.identity, transpose(self.identity)))

    def test_transpose_random(self):
        matrix = []
        for i in range(3):
            matrix.append([random(), random(), random()])

        # Transpose of transpose is equal to original
        matrix_transpose = transpose(matrix)
        matrix_transpose_transpose = transpose(matrix_transpose)
        self.assertTrue(np.allclose(matrix_transpose_transpose, matrix))

        # Determinant of transpose is equal to determinant of original
        self.assertTrue(
            np.allclose(
                compute_determinant_3x3(matrix_transpose),
                compute_determinant_3x3(matrix),
            )
        )

        # (AB)^T == B^TA^T
        A = []
        B = []
        for i in range(3):
            A.append([random(), random(), random()])
            B.append([random(), random(), random()])

        A = np.array(A)
        B = np.array(B)
        AB_t = transpose(A @ B)
        B_tA_t = np.array(transpose(B)) @ np.array(transpose(A))

        self.assertTrue(np.allclose(AB_t, B_tA_t)


if __name__ == "__main__":
    unittest.main()
