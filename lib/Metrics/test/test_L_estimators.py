import unittest
from lib.Metrics.L_estimators import median, Q1,  Q3
import numpy as np
from random import random

class TestUniVariateMetrics(unittest.TestCase):

    def test_median(self):
        data = [random() for _ in range(1000)]
        self.assertTrue(median(data) == np.median(data))
        data = [random() for _ in range(1001)]
        self.assertTrue(median(data) == np.median(data))
  
    def test_Q1(self):
        data = [random() for _ in range(1000)]
        self.assertAlmostEqual(Q1(data), np.quantile(data, 0.25), places=3)
        data = [random() for _ in range(1001)]
        self.assertAlmostEqual(Q1(data), np.quantile(data, 0.25), places=3)

    def test_Q3(self):
        data = [random() for _ in range(1000)]
        self.assertAlmostEqual(Q3(data), np.quantile(data, 0.75), places=3)
        data = [random() for _ in range(1001)]
        self.assertAlmostEqual(Q3(data), np.quantile(data, 0.75), places=3)
    

if __name__ == '__main__':
    unittest.main()