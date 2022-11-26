import numpy as np
import sys
sys.path.append("../2DProjectiveGeometry")
from math_utils import cos, sin, sqrt, atan2, exp, pi

class Prob():
    def __init__(self):
        pass


class NormalDistribution(Prob):
    @staticmethod
    def compute_probability(a, b):
        first = 1 / sqrt(2 * pi * b) 
        second = exp((- a ** 2) / (2 * b))
        return first * second

    """
    Sample from a normal distribution with zero mean
    and b variance.
    """
    @staticmethod
    def sample_probability(b):
        return (b / 6) * sum(np.random.uniform(low = -1, high = 1, size = 12))

class TriangularDistribution(Prob):
    @staticmethod
    def compute_probability(a, b):
        if abs(a) > sqrt(6 * b):
            return 0
        return (sqrt(6 * b) - abs(a)) / (6 * b)

    """
    Sample from a triangular distribution with zero mean
    and b variance.
    """
    @staticmethod
    def sample_probability(b):
        return b * np.random.uniform(low = -1, high = 1) * np.random.uniform(low = -1, high = 1) 
