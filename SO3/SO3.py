import numpy as np

def skew(v):
    return [
        [0, -v[2], v[1]], 
        [v[2], 0, -v[0]],
        [-v[1], v[0], 0]]

def vee(W):
    return [-W[1][2], W[0][2], -W[0][1]]

class SO3():
    def __init__(self, R):
        self.R = R

    def __repr__(self):
        return f"{self.R}"

    def log_map(self):
        """
        Returns the skew matrix in lie algebra associated to the 
        SO3 rotation matrix R
        """
        R = self.R
        A = (R - R.T) / 2
        norm = np.sqrt(-np.trace(A @ A)/2)
        skew_matrix = ((np.arcsin(norm)) / norm) * A
        return so3(vee(skew_matrix))


class so3():
    def __init__(self, w):
        self.w = w # euler angles

    def __repr__(self):
        return f"{self.w}"

    def exp_map_generic(self):
        """
        Simply computes the matrix exponent.
        We should iterate to infinity but we stop at 50.
        """
        A = skew(self.w)
        exp = np.eye(3)
        for k in range(1, 50):
            exp += (1/np.math.factorial(k)) * np.linalg.matrix_power(A, k)
        return SO3(exp)

    def exp_map_euler(self):
        w = np.array(self.w)
        theta = np.linalg.norm(w)
        w = w / theta
        x = w[0]
        y = w[1]
        z = w[2]

        c = np.cos(theta / 2)
        s = np.sin(theta / 2)

        exp = [
            [2*(x**2 - 1)*s**2 + 1, 2*x*y*(s**2) - 2*z*c*s, 2*x*z*s**2 + 2*y*c*s],
            [2*x*y*s**2 + 2*z*c*s, 2*(y**2-1)*s**2+1, 2*y*z*s**2 - 2*x*c*s],
            [2*x*z*s**2 - 2*y*c*s, 2*y*z*s**2 + 2*x*c*s, 2*(z**2-1)*s**2 + 1]
        ]
        return SO3(exp)
