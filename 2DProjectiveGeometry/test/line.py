import unittest
import sys
sys.path.append("..")

from geometry import Line, InhomogeneousPoint


class TestLine(unittest.TestCase):

    def setUp(self):
        self.a0 = 1
        self.b0 = 1
        self.c0 = -5
        self.line1 = Line([self.a0, self.b0, self.c0])

        
    def test_defaultConstructor(self):
        self.assertEqual(self.vector, [self.a0, self.b0, self.c0])


    def test_contains(self):
        """
        Use the line equation to get a point that is
        on the line
        """
        point_on_line =
