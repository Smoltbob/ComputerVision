import unittest
from lib.Transforms.SO3 import SO3_utils
import numpy as np
from scipy.spatial.transform import Rotation as R


class TestUniVariateMetrics(unittest.TestCase):
    def setUp(self):
        self.init_rot = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    def test_constructor(self):
        self.assertTrue(SO3_utils.isValid(self.init_rot))
