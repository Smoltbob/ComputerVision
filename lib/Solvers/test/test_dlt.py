import unittest
from lib.Solvers.dlt import DLT, reproj_error, normalize
import numpy as np

class TestDLT(unittest.TestCase):

    def test_normalize(self):
        norma = lambda x : x / x[:,None,2]

        pts = norma(np.random.random((100,3)))
        P = normalize(pts)

        centroid = np.mean(P@pts.T, axis = 1)
        self.assertTrue(np.allclose(centroid, [0,0,1]))
        average_distance_from_origin = np.linalg.norm((P@pts.T)[0:2], axis = 0).mean()
        self.assertAlmostEqual(average_distance_from_origin, np.sqrt(2))

if __name__ == '__main__':
    unittest.main()