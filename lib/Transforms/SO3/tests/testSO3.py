import unittest
from lib.Transforms.SO3 import SO3
import numpy as np
from scipy.spatial.transform import Rotation as R


class TestUniVariateMetrics(unittest.TestCase):
    def setUp(self):
        self.init_rot = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    def test_constructor(self):
        SO3_1 = SO3.SO3()
        self.assertTrue(np.allclose(self.init_rot, SO3_1.R))

    def test_log_exp_cycle(self):
        for _ in range(100):
            random_rotation = R.random().as_matrix()
            SO3_random1 = SO3.SO3(random_rotation)
            SO3_random2 = SO3_random1.log_map().exp_map_euler()

            self.assertTrue(np.allclose(SO3_random1.R, SO3_random2.R))

    def test_exp_log_cycle(self):
        for _ in range(100):
            random_rotation = R.random().as_rotvec()
            SO3_random1 = SO3.so3(random_rotation)
            SO3_random2 = SO3_random1.exp_map_euler().log_map()

            self.assertTrue(np.allclose(SO3_random1.w, SO3_random2.w))


if __name__ == "__main__":
    unittest.main()