import unittest
from lib.Metrics.univariate_metrics import median
import numpy as np
from random import random

class TestUniVariateMetrics(unittest.TestCase):

    def test_median(self):
        data = [random() for _ in range(1000)]
        self.assertTrue(median(data) == np.median(data))
        data = [random() for _ in range(1001)]
        self.assertTrue(median(data) == np.median(data))

if __name__ == '__main__':
    unittest.main()