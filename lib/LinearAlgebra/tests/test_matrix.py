import unittest
from lib.LinearAlgebra import matrix
from random import random
import numpy as np

class TestMatrix(unittest.TestCase):

    def setUp(self):
        self.identity = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    def test_constructor(self):
        self.assertTrue(np.allclose(self.identity, matrix.transpose(self.identity)))

    def test_with_random(self):
        matrix = []
        for i in range(3):
            matrix[i] = [random(), random(), random()]
        
        matrix_transpose = matrix.transpose(matrix)
        matrix_transpose_transpose = matrix.transpose(matrix_transpose)
        self.assertTrue(np.allclose(matrix_transpose_transpose, matrix))


if __name__ == '__main__':
    unittest.main()