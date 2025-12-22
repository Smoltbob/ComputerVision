import numpy as np
import PIL 

# Create Dummy Checkered Images for Omnidirectional Camera Simulation
def create_checkered_image(width, height, color1, color2, grid_size=10):
    img = np.zeros((height, width, 3), dtype=np.uint8)
    # Fill background
    img[:] = color1
    step_x = width // grid_size
    step_y = height // grid_size
    # Draw checkers
    for y in range(0, height, step_y):
        for x in range(0, width, step_x):
            if ((x // step_x) + (y // step_y)) % 2 == 0:
                img[y:y+step_y, x:x+step_x] = color2
    return img


def get_sync_fisheye_cameras():

    img1 = create_checkered_image(400, 400, (255, 0, 0), (0, 255, 0), grid_size=8)  # Red-Green
    img2 = create_checkered_image(400, 400, (0, 0, 255), (255, 255, 0), grid_size=8)  # Blue-Yellow
    img3 = create_checkered_image(400, 400, (255, 0, 255), (0, 255, 255), grid_size=8)  # Magenta-Cyan
    img4 = create_checkered_image(400, 400, (192, 192, 192), (64, 64, 64), grid_size=8)  # Silver-Gray

    camera_config = [
        {"image": img1, "yaw_rotation": 0},
        {"image": img2, "yaw_rotation": 180},
        {"image": img3, "yaw_rotation": 90},
        {"image": img4, "yaw_rotation": 270}
    ]

    return camera_config

def get_images():
    # Load images from Data Directory
    img1 = np.array(PIL.Image.open('/app/lib/CameraModels/OmnidirectionalModel/Data/0_front.png'))
    img2 = np.array(PIL.Image.open('/app/lib/CameraModels/OmnidirectionalModel/Data/0_rear.png'))
    img3 = np.array(PIL.Image.open('/app/lib/CameraModels/OmnidirectionalModel/Data/0_left.png'))
    img4 = np.array(PIL.Image.open('/app/lib/CameraModels/OmnidirectionalModel/Data/0_right.png'))

    bgr_to_rgb = lambda img: img[:, :, ::-1]
    img1 = bgr_to_rgb(img1)
    img2 = bgr_to_rgb(img2)
    img3 = bgr_to_rgb(img3)
    img4 = bgr_to_rgb(img4)

    camera_config = [
        {"image": img1, "yaw_rotation": 0},
        {"image": img2, "yaw_rotation": 180},
        {"image": img3, "yaw_rotation": 90},
        {"image": img4, "yaw_rotation": 270}
    ]   
    return camera_config