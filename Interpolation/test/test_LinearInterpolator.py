import unittest
from Interpolation.LinearInterpolation import LinearInterpolator
from ProjectiveGeometry.geometry import Point

class TestLinearInterpolator(unittest.TestCase):

    def setUp(self):
        ptA = Point(0, 0)
        ptB = Point(1, 1)
        self.linear_interpolator = LinearInterpolator(ptA, ptB)

        
    def test_interpolatescorrectly(self):
        x = 0.5
        self.assertEqual(self.linear_interpolator.interpolate(x), x)

if __name__ == '__main__':
    unittest.main()