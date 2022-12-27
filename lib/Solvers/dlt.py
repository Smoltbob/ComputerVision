# Implement all that is needed for the DLT and unit test it
import numpy as np

norma = lambda x : x / x[:,None,2]

def normalize(points):
    """
    Normalizes / Pre-conditions the set of points for the DLT.
    The points are 2D homogeneous.

    Computes a 3x3 matrix T such that with P = T @ points 
    1. The points are translated so that their centroid 
    is at the origin
    2. The points are scaled so that the average distance
    from the origin is sqrt(2)

    See https://www.cse.unr.edu/~bebis/CS485/Handouts/hartley.pdf

    T = [[1/s, 0, -cx/s], [0, 1/s, -cy/s], [0, 0, 1]]
    with s = scale_factor, cx = centroid(0), cy = centroid(1)
    """
    centroid = np.mean(points, axis = 0)
    points_translated = points - [centroid[0], centroid[1], 0]
    
    a = np.linalg.norm(points_translated[:, 0:2], axis = 1).mean()
 
    factor = np.sqrt(2) / a
    
    norm_T = np.eye(3) 
    norm_T[:,2] = -centroid
    norm_T *= factor
    norm_T[-1,-1] = 1

    return norm_T

def reproj_error(a, b, H):
    return np.linalg.norm((b - norma((H @ a.T).T)), axis=1)


def DLT(points_1, points_2):
    """
    Simple homography computation using the DLT.
    We minimise the norm ||Ah|| with |h| = 1, because
    ideally we want Ah=0.
    The solution is the unit singular vector corresponding
    to the smallest singular value of A.
    A: matrix with the point correspondance constraints (size 2N x 9)
        (N: number of point correspondances)
    h: homography coefficients (9 x 1)
    """
    assert len(points_1) == len(points_2)
    T = normalize(points_1)
    Tp = normalize(points_2)
    
    points_1 = norma(points_1 @ T.T)
    points_2 = norma(points_2 @ Tp.T)

    A = np.hstack([np.hstack([np.zeros_like(points_1), -points_1, points_1 * points_2[:,1][:,None]]),
           np.hstack([points_1, np.zeros_like(points_1), -points_1 * points_2[:,0][:,None]])]).reshape([-1,9])
    
    # 2. Compute SVD of A
    u, s, v = np.linalg.svd(A)
    # 3. Then h is the last column of v 
    H = v[-1, :].reshape(3, 3)
    H = np.linalg.inv(Tp) @ (H @ T)
    H = H / H[-1,-1]
    return H