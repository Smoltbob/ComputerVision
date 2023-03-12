import unittest
from lib.Transforms.SO3.SO3 import SO3
from lib.Transforms.so3.so3 import so3
from lib.Transforms.s3.s3 import S3
from lib.Transforms.conversions.conversions import (
    SO3_from_S3,
    S3_from_SO3,
    log_to_SO3,
    SO3_to_log,
)
import numpy as np
from scipy.spatial.transform import Rotation as R


class TestConversions(unittest.TestCase):
    def setUp(self):
        self.identity_SO3 = SO3([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        self.identity_S3 = S3([1, 0, 0, 0])

    def test_SO3_from_S3_identity_transforms(self):
        converted_SO3_from_S3 = SO3_from_S3(self.identity_S3)
        self.assertTrue(
            np.allclose(converted_SO3_from_S3.R, self.identity_SO3.R)
        )

    def test_SO3_from_S3_and_back_random_transforms(self):
        for _ in range(100):
            random_q = S3(np.random.rand(4))
            converted_SO3_from_S3 = SO3_from_S3(random_q)
            converted_S3_from_SO3 = S3_from_SO3(converted_SO3_from_S3)

            self.assertTrue(np.allclose(random_q.w, converted_S3_from_SO3.w))

    def test_S3_from_S03_and_back_random_transforms(self):
        for _ in range(100):
            random_R = SO3(R.random().as_matrix())
            converted_S3_from_SO3 = S3_from_SO3(random_R)
            converted_SO3_from_S3 = SO3_from_S3(converted_S3_from_SO3)

            self.assertTrue(np.allclose(random_R.R, converted_SO3_from_S3.R))

    # Log Maps
    def test_log_exp_cycle(self):
        for _ in range(100):
            random_rotation = R.random().as_matrix()
            SO3_random1 = SO3(random_rotation)
            SO3_random2 = log_to_SO3(SO3_to_log(SO3_random1))
            self.assertTrue(np.allclose(SO3_random1.R, SO3_random2.R))

    def test_exp_log_cycle(self):
        for _ in range(100):
            random_rotation = R.random().as_rotvec()
            SO3_random1 = so3(random_rotation)
            SO3_random2 = SO3_to_log(log_to_SO3(SO3_random1))
            self.assertTrue(np.allclose(SO3_random1.w, SO3_random2.w))


if __name__ == "__main__":
    unittest.main()
