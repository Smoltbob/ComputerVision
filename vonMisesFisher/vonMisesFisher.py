from lib.Math.constants import pi, e
from lib.Math.math_utils import exp, dot, log, sqrt
from lib.Transforms.CircleGroup.S1 import S1
import random

class vMF:

    @staticmethod
    def pdf(mu, kappa, omega):
        """
        Parameters:
        - mu = 3-vector giving the mean
        - kappa = concentration coefficient (close to zero = uniform distribution)
        - omega = input 3-vector

        Returns:
        Probability of omega to come from the distribution.
        """
        assert(kappa >= 0)
        if kappa == 0:
            return 1 / (4*pi)
        
        denum = 2 * pi * (1 - exp(-2 * kappa))
        frac = kappa / denum
        
        return frac * (e**(kappa * (dot(mu, omega) -1)))

    @staticmethod
    def F_inverse(kappa, xi):
        """
        Returns the float W required to sample from the vMF

        Parameters:
        - kappa = concentration coefficient (close to zero = uniform distribution)
        - xi a random float between 0 and 1
        """
        # Numerically stable version
        invkappa = 1 / kappa
        A = xi + (1 - xi) * (e **(-2*kappa))
        return 1 + invkappa * log(A)


    @staticmethod
    def samplevMF(kappa):
        """
        Samples from a vMF distribution of mean [0,0,1] and concentration kappa
        Ref: http://www.mitsuba-renderer.org/~wenzel/files/vmf.pdf
        """
        angle = random.uniform(0, 2*pi)
        v = S1(angle)
        x, y = v.z.r, v.z.i
        W = vMF.F_inverse(kappa, random.random())
        fact = sqrt(1-W**2)
        omega = [fact * x, fact * y, W]
        return omega 
