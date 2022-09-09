import unittest
import sys
sys.path.append("..")

from geometry import Line, HomogeneousPoint


class TestLine(unittest.TestCase):

    def setUp(self):
        self.a0 = 1
        self.b0 = 1
        self.c0 = -5
        self.line1 = Line([self.a0, self.b0, self.c0])
        self.point1 = HomogeneousPoint([1, 4, 1]) # TODO compute from line equation
        self.point2 = HomogeneousPoint([0, 6, 1])

        
    def test_defaultConstructor(self):
        self.assertEqual(self.line1.vector, [self.a0, self.b0, self.c0])

    def test_contains(self):
        """
        Use the line equation to get a point that is
        on the line
        """
        self.assertTrue(self.point1 in self.line1)
        self.assertFalse(self.point2 in self.line1)

    def test_intersection(self):
        pass


if __name__ == '__main__':
    unittest.main()