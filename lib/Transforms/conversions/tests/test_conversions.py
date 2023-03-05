import unittest
from lib.Transforms.SO3.SO3 import SO3
from lib.Transforms.s3.s3 import S3
from lib.Transforms.conversions.conversions import SO3_from_S3
import numpy as np
from scipy.spatial.transform import Rotation as R


class TestConversions(unittest.TestCase):
    def setUp(self):
        self.identity_SO3 = SO3([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        self.identity_S3 = S3([1, 0, 0, 0])

    def test_identity_transforms(self):
        converted_SO3_from_S3 = SO3_from_S3(self.identity_S3)
        self.assertTrue(np.allclose(converted_SO3_from_S3.R, self.identity_SO3.R))


if __name__ == "__main__":
    unittest.main()
