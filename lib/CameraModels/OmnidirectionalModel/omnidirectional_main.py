# Implementation of an Omnidirectional Camera Model

# Main features:
# 1. Projection of 3D points onto the image plane considering omnidirectional distortion
# 2. Back-projection of image points to 3D rays
# 3. Handling of intrinsic parameters specific to omnidirectional cameras

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
from matplotlib import pyplot as plt
import lib.CameraModels.OmnidirectionalModel.data_production as data_production
import lib.CameraModels.OmnidirectionalModel.omnidirectional_model as omni_model

import numpy as np


# --- NEW HELPER: Generate Flat Image Plane ---
def generate_flat_sensor_plane(image, width_in_world_units=2.0):
    """
    Creates a 3D point cloud representing the flat 2D image.
    Used to show the original image plane in 3D space.
    """
    height, width, _ = image.shape
    aspect_ratio = height / width
    
    # 1. Generate Grid
    u, v = np.meshgrid(np.arange(width), np.arange(height))
    
    # 2. Normalize to World Units (Center at 0,0)
    # Map u (0 to width) -> x (-1 to 1)
    x = (u - width / 2) / width * width_in_world_units
    # Map v (0 to height) -> y (-ratio to ratio)
    y = (v - height / 2) / width * width_in_world_units 
    
    # 3. Z-coordinate is 0 for now (flat plane)
    z = np.zeros_like(x)
    
    # 4. Stack and reshape
    flat_vectors = np.dstack((x, y, z)).reshape(-1, 3)
    
    # 5. Get Colors just like before
    colors_int = image[v.flatten(), u.flatten()]
    colors = colors_int[:, [2, 1, 0]].astype(np.float64) / 255.0
    
    return flat_vectors, colors

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

def project_cloud_oriented(points, colors, rotation=(0,0,0), 
                           focal_length=0.06, sensor_size=(10.5, 10.5)):
    """
    Projects sphere points onto a rotated plane tangent to the sphere.
    rotation: tuple (yaw, pitch, roll) in degrees.
    """
    def rotate_and_filter_points(rotation, points, colors):
        # 1. Get Rotation Matrix
        yaw, pitch, roll = rotation
        R = get_rotation_matrix(yaw, pitch, roll)
        
        # --- CORE LOGIC: Inverse Rotation ---
        # We want to know: "If I rotate my camera by R, what does it see?"
        # Mathematically, this is equivalent to rotating the WORLD by R_inverse.
        # Since R is orthogonal, Inverse = Transpose.
        
        # Rotate the sphere points into the "Camera View" frame
        # v_camera = R_inv * v_world
        R_inv = R.T
        points_in_cam_frame = np.dot(R_inv, points.T).T
        
        x_c = points_in_cam_frame[:, 0]
        y_c = points_in_cam_frame[:, 1]
        z_c = points_in_cam_frame[:, 2]
        
        # 3. Filter: Only keep points in front of the rotated camera (Z_c > 0)
        valid_mask = z_c > 0.1

        x_c = x_c[valid_mask]
        y_c = y_c[valid_mask]
        z_c = z_c[valid_mask]
        valid_colors = colors[valid_mask]

        return x_c, y_c, z_c, valid_colors
    
    # 1. Rotate and Filter Points
    x_c, y_c, z_c, valid_colors = rotate_and_filter_points(rotation, points, colors)

    # 4. Project (Standard Pinhole in Camera Frame)
    u = focal_length * (x_c / z_c)
    v = focal_length * (y_c / z_c)
    
    # 5. Crop to Sensor
    w, h = sensor_size
    sensor_mask = (np.abs(u) <= w/2) & (np.abs(v) <= h/2)
    
    u = u[sensor_mask]
    v = v[sensor_mask]
    final_colors = valid_colors[sensor_mask]
    
    def move_plane_to_world(u, v, R, focal_length):
        # 6. Reconstruct the 3D Plane for Visualization
        # We have (u, v) on the flat 2D sensor. We need to put them back into 3D World Space.
        
        # A. Place on flat plane at Z=1 (Tangent distance)
        # In camera frame: (u, v, focal_length) -> scaled to distance 1.0
        # Wait! If we want TANGENT, the plane distance is fixed at 1.0.
        # The focal length determines FOV, but the physical placement is Z=1.
        
        # Let's assume physical distance D = 1.0
        D = 2.0
        scale = D / focal_length
        
        x_flat_cam = u * scale
        y_flat_cam = v * scale
        z_flat_cam = np.full_like(x_flat_cam, D)
        
        flat_cam_vectors = np.dstack((x_flat_cam, y_flat_cam, z_flat_cam)).reshape(-1, 3)
        
        # B. Rotate the plane BACK to World Space
        # v_world = R * v_camera
        flat_world_vectors = np.dot(R, flat_cam_vectors.T).T

        return flat_world_vectors

    flat_world_vectors = move_plane_to_world(u, v, get_rotation_matrix(*rotation), 8)
    
    return flat_world_vectors, final_colors

# --- STEP 2 Logic: Rotation ---
def get_rotation_matrix_y(degrees):
    radians = np.radians(degrees)
    cos_a = np.cos(radians)
    sin_a = np.sin(radians)
    R = np.array([
        [ cos_a, 0, sin_a],
        [     0, 1,     0],
        [-sin_a, 0, cos_a]
    ])
    return R

# --- Main Simulation ---
if __name__ == "__main__":
    # Settings
    FOV = 190 # Slightly over 180 to ensure overlap
    SENSOR_DISTANCE = 1

    print("1. Generating dummy fisheye images...")
    # Define our multi-camera setup config
    camera_config = data_production.get_images()#get_sync_fisheye_cameras()

    global_points = []
    global_colors = []

    print("2. Processing cameras (Unprojecting and Rotating)...")
    for i, cam in enumerate(camera_config):
        print(f"   Processing camera {i+1}...")
        # A. Unproject to local camera space
        local_vectors, colors = omni_model.unproject_and_sample_colors(cam["image"], FOV)
        
        # B. Get rotation for this camera orientation
        R = get_rotation_matrix_y(cam["yaw_rotation"])
        
        # C. Apply rotation to move to World Space
        # np.dot(R, v.T).T performs R * v for every vector v in the list
        world_vectors = np.dot(R, local_vectors.T).T
        
        global_points.append(world_vectors)
        global_colors.append(colors)

        if False:
            # --- PART 2: The Flat Sensor Plane (New Logic) ---
            print(f"   Adding flat plane for camera {i+1}...")
            flat_vectors, flat_colors = generate_flat_sensor_plane(cam["image"])
            
            # We need to orient the flat plane to match the camera
            # 1. Rotate the flat plane
            flat_vectors_rotated = np.dot(R, flat_vectors.T).T
            
            # 2. Push the plane "backward" relative to where the camera is looking.
            # If camera looks down Z+, we push plane to Z-.
            # We can calculate the "backward" vector by rotating a simple [0, 0, -1] vector.
            backward_vector = np.dot(R, np.array([0, 0, -SENSOR_DISTANCE]))
            
            # Add this translation to all points
            flat_vectors_final = flat_vectors_rotated + backward_vector
            
            global_points.append(flat_vectors_final)
            global_colors.append(flat_colors)

    # Consolidate all lists into huge numpy arrays
    all_points_np = np.vstack(global_points)
    all_colors_np = np.vstack(global_colors)
    print(f"Total points generated: {len(all_points_np)}")

    print("2bis. Projecting Sphere to Flat Plane (Rectilinear)...")
    
    # Project the points
    # focal_length controls the FOV of the virtual camera. 
    # Lower f = Wide Angle (more distortion at edges). Higher f = Zoom.
    views = [
        (10, -80, 0), # yaw, pitch, roll
       # (30, -20, 0),
       # (-60, -30, 0)
    ]
    planes_views = []
    plane_colors_views = []
    for view in views:
        yaw, pitch, roll = view
        plane_vectors, plane_colors = project_cloud_oriented(all_points_np, all_colors_np, rotation=(yaw, pitch, roll), focal_length=1.0)
        planes_views.append(plane_vectors)
        plane_colors_views.append(plane_colors)

    all_points_np = np.vstack([all_points_np, *planes_views])
    all_colors_np = np.vstack([all_colors_np, *plane_colors_views])
    print(f"Total points after adding projected planes: {len(all_points_np)}")

    # Go from Y down, Z forward to Z up, Y forward
    R_x_minus_90 = np.array([
        [1, 0, 0],
        [0, 0, 1],   # cos(-90)=0, -sin(-90)=1
        [0, -1, 0]   # sin(-90)=-1, cos(-90)=0
    ])
    all_points_np = np.dot(R_x_minus_90, all_points_np.T).T

    print("3. Plotting the combined point cloud...")
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(all_points_np[:,0], all_points_np[:,1], all_points_np[:,2], c=all_colors_np, s=0.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Omnidirectional Camera Point Cloud')
    ax.set_box_aspect([1,1,1])  # Equal aspect ratio
    plt.savefig('/app/output/omnidirectional_point_cloud.png')


def render_virtual_view(points, colors, yaw_deg, pitch_deg, output_size=(800, 800), fov_deg=90):
    """
    Projects the 3D point cloud onto a 2D plane (Virtual Pinhole Camera).
    """
    W, H = output_size
    f = (W / 2.0) / np.tan(np.radians(fov_deg / 2.0))
    cx, cy = W / 2.0, H / 2.0

    # 1. Create Rotation Matrix for the Camera View
    # We combine Yaw (Y-axis) and Pitch (X-axis)
    # Note: We need the Inverse rotation to move points INTO the camera frame.
    # R_cam = R_yaw * R_pitch. 
    # To transform points: P_cam = P_world * R_cam (if using row vectors)
    # Actually, to align world to camera, we need P_cam = P_world * R_cam_inverse
    
    # Rotation X (Pitch)
    rx_rad = np.radians(pitch_deg)
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(rx_rad), -np.sin(rx_rad)],
        [0, np.sin(rx_rad), np.cos(rx_rad)]
    ])
    
    # Rotation Y (Yaw)
    ry_rad = np.radians(yaw_deg)
    Ry = np.array([
        [np.cos(ry_rad), 0, np.sin(ry_rad)],
        [0, 1, 0],
        [-np.sin(ry_rad), 0, np.cos(ry_rad)]
    ])
    
    # Combined Rotation (Order matters: usually Yaw then Pitch)
    R_cam = Ry @ Rx
    
    # Invert rotation to transform points relative to camera
    # (For rotation matrices, Inverse == Transpose)
    R_view = R_cam.T

    # 2. Rotate Points
    # vectors (N, 3) @ Matrix (3, 3)
    points_cam = points @ R_view.T 

    # 3. Filter points behind the camera
    # We only want points where Z > 0 (in front of camera)
    # Adding a small epsilon 0.1 to avoid divide by zero
    valid_mask = points_cam[:, 2] > 0.1
    
    p_valid = points_cam[valid_mask]
    c_valid = colors[valid_mask]

    if len(p_valid) == 0:
        return np.zeros((H, W, 3), dtype=np.uint8)

    # 4. Perspective Projection
    x = p_valid[:, 0]
    y = p_valid[:, 1]
    z = p_valid[:, 2]
    
    u = (f * (x / z) + cx).astype(int)
    v = (f * (y / z) + cy).astype(int)

    # 5. Filter points outside the screen boundaries
    screen_mask = (u >= 0) & (u < W) & (v >= 0) & (v < H)
    
    u_final = u[screen_mask]
    v_final = v[screen_mask]
    c_final = c_valid[screen_mask]

    # 6. Rasterize (Draw points on black canvas)
    # Initialize black image
    canvas = np.zeros((H, W, 3), dtype=np.uint8)
    
    # Convert colors from 0.0-1.0 float to 0-255 int
    c_final_int = (c_final * 255).astype(np.uint8)
    
    # Assign colors. 
    # Note: If multiple points hit the same pixel, this simple method 
    # just overwrites. (Painter's algorithm isn't strictly necessary for sparse clouds)
    canvas[v_final, u_final] = c_final_int
    
    return canvas

# --- USAGE EXAMPLE (Add this to the end of the previous main block) ---
# Assuming 'all_points_np' and 'all_colors_np' exist from the previous step:

print("4. Rendering Virtual Camera View...")
# Look 45 degrees to the right, slightly up
virtual_photo = render_virtual_view(all_points_np, all_colors_np, 
                                    yaw_deg=45, pitch_deg=-10, 
                                    output_size=(640, 480), fov_deg=100)

# Save the virtual view
plt.imsave('/app/output/virtual_camera_view.png', virtual_photo)