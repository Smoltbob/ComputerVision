import unittest
import sys
sys.path.append("..")
import Complex

class TestComplex(unittest.TestCase):

    def setUp(self):
        """
        TODO use random
        """
        self.r1 = 1
        self.i1 = 2
        self.cplx1 = Complex.Complex(self.r1, self.i1)
        self.cplx1_2 = Complex.Complex(self.r1, self.i1)

        self.r2 = 3
        self.i2 = 4
        self.cplx2 = Complex.Complex(self.r2, self.i2)

        
    def test_defaultConstructor(self):
        self.assertEqual(self.cplx1.r, self.r1)
        self.assertEqual(self.cplx1.i, self.i1)

    def test_eq(self):
        self.assertEqual(self.cplx1, self.cplx1_2)
        self.assertNotEqual(self.cplx1, self.cplx2)

    def test_conjugate(self):
        conjugate = self.cplx1.conjugate()
        self.assertEqual(self.cplx1.r, conjugate.r)
        self.assertEqual(self.cplx1.i, -conjugate.i)

        # The conjugate does not change the norm
        conjugate_conjugate = conjugate.conjugate()
        self.assertEqual(self.cplx1, conjugate_conjugate)
        
        # The conjugate affects the angle, modulo 2pi
        self.assertEqual(self.cplx1.magnitude(), conjugate.magnitude())
        self.assertEqual(self.cplx1.angle(), -conjugate.angle())


if __name__ == '__main__':
    unittest.main()
