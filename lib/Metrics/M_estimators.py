import numpy as np

def make_vandermonde(data, degree):
    # Implements  # X = np.vander(data, degree)
    size = len(data)
    X = np.zeros((size, degree))
    for i in range(size):
        for d in range(degree):
            X[i][degree-1-d] =  data[i] ** d
    return X


def ordinary_least_squares(data_y, degree):
    """
    Considering equations y = beta_degree * x **degree + ... + beta_0 * x **0,
    estimate the vector of betas.
    """
    size = len(data_y) #number of data points
    p = degree + 1 # degree 0 = 1 constant regressor
    data_x = [x for x in range(size)]
    X = make_vandermonde(data_x, p)     # Build the n x p X matrix
    beta = (np.linalg.inv(X.T @ X) @ X.T) @ data_y # Highly ineficient for large matrices
    return beta
