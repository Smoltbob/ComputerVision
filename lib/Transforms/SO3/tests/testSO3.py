import unittest
from lib.Transforms.SO3 import SO3
import numpy as np

class TestUniVariateMetrics(unittest.TestCase):

    def setUp(self):
        self.init_rot = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    def test_constructor(self):

        SO3_1 = SO3.SO3()
        self.assertTrue(np.allclose(self.init_rot, SO3_1.R))

    

if __name__ == '__main__':
    unittest.main()