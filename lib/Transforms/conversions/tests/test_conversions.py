import unittest
from lib.Transforms.SO3 import SO3
from lib.Transforms.s3.s3 import S3
from lib.Transforms.conversions import *
import numpy as np
from scipy.spatial.transform import Rotation as R


class TestConversions(unittest.TestCase):
    def setUp(self):
        self.init_rot = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    def test_constructor(self):

        self.assertTrue(True)
