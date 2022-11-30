import unittest
import sys
sys.path.append("..")

from geometry import Line, HomogeneousPoint


class TestLine(unittest.TestCase):

    def setUp(self):
        self.a0 = 1
        self.b0 = 1
        self.c0 = -5
        self.line0 = Line([self.a0, self.b0, self.c0])
        self.point1 = HomogeneousPoint([1, 4, 1]) # TODO compute from line equation
        self.point2 = HomogeneousPoint([0, 6, 1])

        self.a1 = -1
        self.b1 = 2
        self.c1 = 1
        self.line1 = Line([self.a1, self.b1, self.c1])

        
    def test_defaultConstructor(self):
        self.assertEqual(self.line0.vector, [self.a0, self.b0, self.c0])

    def test_contains(self):
        """
        Use the line equation to get a point that is
        on the line
        """
        self.assertTrue(self.point1 in self.line0)
        self.assertFalse(self.point2 in self.line0)

    def test_intersection(self):
        intersection = self.line0.intersection(self.line1)
        self.assertEqual(intersection.vector, [11, 4, 3])


if __name__ == '__main__':
    unittest.main()