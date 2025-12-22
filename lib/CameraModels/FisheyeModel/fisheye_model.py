import numpy as np
import matplotlib.pyplot as plt

# AI generated, not reviewed
def project_fisheye(points_3d, f, cx, cy):
    """
    Projects 3D points (X, Y, Z) onto a 2D image plane using the 
    Equidistant fisheye model: r = f * theta
    """
    # 1. Extract coordinates
    X = points_3d[:, 0]
    Y = points_3d[:, 1]
    Z = points_3d[:, 2]
    
    # 2. Convert 3D Cartesian to Spherical (Theta, Phi)
    # Calculate the distance in the XY plane (distance from optical axis)
    r_xy = np.sqrt(X**2 + Y**2)
    
    # Theta (Incident Angle): Angle off the Z-axis
    theta = np.arctan2(r_xy, Z)
    
    # Phi (Azimuth): Direction in the XY plane ('clock face' direction)
    phi = np.arctan2(Y, X)
    
    # 3. Apply Fisheye Mapping (The "r" calculation)
    # Using Equidistant model: r_image = f * theta
    r_image = f * theta
    
    # 4. Convert Polar (r_image, phi) back to Cartesian Image Coordinates (u, v)
    # Note: We add cx, cy to move the origin from top-left to image center
    u = cx + r_image * np.cos(phi)
    v = cy + r_image * np.sin(phi)
    
    return np.column_stack((u, v))

# --- Setup Simulation ---

# Camera Intrinsics
focal_length = 300  # pixels
center_x = 400      # image center x
center_y = 300      # image center y

# Define 3D points (X, Y, Z)
# Z is forward. Points are located 1 meter in front of the camera.
points_world = np.array([
    [0, 0, 1],      # Center point
    [1, 0, 1],      # Right (3 o'clock)
    [0, 1, 1],      # Top (12 o'clock)
    [-1, -1, 1],    # Bottom-Left diagonal
    [10, 0, 1],     # Far Right (Extreme wide angle)
])

# Run Projection
pixels = project_fisheye(points_world, focal_length, center_x, center_y)

# --- Display Results ---
print(f"{'3D Point (X,Y,Z)':<20} | {'Angle (deg)':<12} | {'Pixel (u, v)'}")
print("-" * 60)

for P, uv in zip(points_world, pixels):
    # Calculate angle just for display purposes
    angle_deg = np.degrees(np.arctan2(np.linalg.norm(P[:2]), P[2]))
    print(f"{str(P):<20} | {angle_deg:<12.1f} | {np.round(uv, 1)}")

# Visualization
plt.figure(figsize=(6, 4))
plt.scatter(pixels[:, 0], pixels[:, 1], c='red', label='Projected Points')
plt.scatter([center_x], [center_y], marker='x', c='blue', label='Image Center')
plt.xlim(0, 800); plt.ylim(600, 0) # Set image bounds (0,0 is top left)
plt.grid(True, linestyle='--')
plt.title("Fisheye Projection on Sensor")
plt.xlabel("u (pixels)"); plt.ylabel("v (pixels)")
plt.legend()
plt.show()