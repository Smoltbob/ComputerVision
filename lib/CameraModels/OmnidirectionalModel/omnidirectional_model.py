# Project points from 3D points in the camera frame to 2D image pixels
# using an omnidirectional camera model.

import numpy as np

def get_rotation_matrix(yaw, pitch, roll):
    """
    Returns a 3x3 Rotation Matrix combining Yaw (Y), Pitch (X), and Roll (Z).
    Angles are in degrees.
    Order of operations: R = Rz * Ry * Rx
    """
    # Convert to radians
    alpha, beta, gamma = np.radians(pitch), np.radians(yaw), np.radians(roll)

    # Rotation around X-axis (Pitch)
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(alpha), -np.sin(alpha)],
        [0, np.sin(alpha), np.cos(alpha)]
    ])

    # Rotation around Y-axis (Yaw)
    Ry = np.array([
        [np.cos(beta), 0, np.sin(beta)],
        [0, 1, 0],
        [-np.sin(beta), 0, np.cos(beta)]
    ])

    # Rotation around Z-axis (Roll)
    Rz = np.array([
        [np.cos(gamma), -np.sin(gamma), 0],
        [np.sin(gamma), np.cos(gamma), 0],
        [0, 0, 1]
    ])

    # Combined Rotation
    R = Rz @ Ry @ Rx
    return R

def project_omnidirectional(points_3d, f, cx, cy, xi):
    """
    Projects 3D points (X, Y, Z) onto a 2D image plane using the 
    Omnidirectional camera model.
    """
    # 1. Extract coordinates
    X = points_3d[:, 0]
    Y = points_3d[:, 1]
    Z = points_3d[:, 2]
    
    # 2. Convert 3D Cartesian to Spherical (Theta, Phi)
    r_xy = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(r_xy, Z)
    phi = np.arctan2(Y, X)
    
    # 3. Apply Omnidirectional Mapping
    d = np.sqrt(X**2 + Y**2 + Z**2)
    r_image = f * (theta / (1 + xi * (d - Z) / d))
    
    # 4. Convert Polar (r_image, phi) back to Cartesian Image Coordinates (u, v)
    u = cx + r_image * np.cos(phi)
    v = cy + r_image * np.sin(phi)
    
    return np.column_stack((u, v))

def unproject(K, D, xi, x, y):
    """
    Takes 2D image pixels and converts them to 3D unit vectors

    K: Intrinsic matrix
    D: Distortion coefficients
    xi: Offset of the projection center along the Z-axis
    x and y: pixel coordinates
    """
    import cv2
    points_2d = np.column_stack((x, y)).astype(np.float32)
    points_3d = cv2.omnidir.undistortPoints(points_2d, K, D, xi, np.eye(3))
    # Convert to unit vectors
    points_3d /= np.linalg.norm(points_3d, axis=1, keepdims=True)
    return points_3d

def unproject_and_sample_colors(image, fov_degrees):
    """
    Converts image pixels to 3D unit vectors and samples their colors.
    Returns:
        vectors: (N, 3) numpy array of XYZ coordinates
        colors: (N, 3) numpy array of RGB values normalized to [0.0, 1.0]
    """
    height, width, _ = image.shape
    
    # 1. Define Camera Intrinsics (Approximate focal length based on FOV)
    # Using Equidistant model: r = f * theta
    # Max theta is FOV/2. Max r is width/2.
    max_theta_rad = np.radians(fov_degrees / 2.0)
    f = (width / 2.0) / max_theta_rad
    cx, cy = width / 2.0, height / 2.0
    
    # 2. Generate Grid
    u_grid, v_grid = np.meshgrid(np.arange(width), np.arange(height))
    
    # Flatten arrays for easier vector processing (N, 1)
    u = u_grid.flatten()
    v = v_grid.flatten()

    # 3. Center coordinates
    u_norm = u - cx
    v_norm = v - cy
    
    # 4. Calculate Radius (r) and Theta
    r = np.sqrt(u_norm**2 + v_norm**2)
    theta = r / f
    
    # --- Optimization: Mask pixels outside the FOV circle ---
    # Pixels in the corners of the square image aren't valid fisheye data.
    valid_mask = r <= (width / 2.0)
    
    # Apply mask to keep only valid pixels
    u_valid = u[valid_mask]
    v_valid = v[valid_mask]
    theta_valid = theta[valid_mask]
    u_norm_valid = u_norm[valid_mask]
    v_norm_valid = v_norm[valid_mask]

    # 5. Convert to 3D Cartesian (Optical axis is Z+)
    phi = np.arctan2(v_norm_valid, u_norm_valid)
    
    x = np.sin(theta_valid) * np.cos(phi)
    y = np.sin(theta_valid) * np.sin(phi)
    z = np.cos(theta_valid)
    
    vectors = np.dstack((x, y, z)).reshape(-1, 3)
    
    # 6. Sample Colors
    # IMPORTANT: Image indexing is img[row, col] which is img[v, u]
    colors_int = image[v_valid, u_valid]
    # Convert BGR (OpenCV default) to RGB (Open3D default)
    colors_rgb = colors_int[:, [2, 1, 0]]
    colors_normalized = colors_rgb.astype(np.float64) / 255.0
    
    return vectors, colors_normalized