from typing import Any, Tuple
from lib.Transforms.SE3 import Se3
import numpy as np

def try_triangulate_point(source_from_world: Se3,
                          target_from_world: Se3,
                          source_ray: Any,
                          target_ray: Any) -> Tuple[bool, Any]:
    """
    Attempts to triangulate a 3D point from two rays in different camera frames.

    Args:
        source_from_world: Extrinsics of the source camera (Se3).
        target_from_world: Extrinsics of the target camera (Se3).
        source_ray: 3D ray from the source camera.
        target_ray: 3D ray from the target camera.
    """
    source_matrix = source_from_world.getMatrix3x4()
    target_matrix = target_from_world.getMatrix3x4()

    src_x = source_ray[0]
    src_y = source_ray[1]
    src_w = source_ray[2]

    tgt_x = target_ray[0]
    tgt_y = target_ray[1]
    tgt_w = target_ray[2]

    matrix = np.array([
        src_x * source_matrix[2, :] - src_w * source_matrix[0, :],
        src_y * source_matrix[2, :] - src_w * source_matrix[1, :],
        tgt_x * target_matrix[2, :] - tgt_w * target_matrix[0, :],
        tgt_y * target_matrix[2, :] - tgt_w * target_matrix[1, :]
    ])

    _, _, vt = np.linalg.svd(matrix)
    point_homogeneous = vt[-1]
    if abs(point_homogeneous[3]) < 1e-6:
        return False, None  # Cannot triangulate
    point_3d = point_homogeneous / point_homogeneous[3]
    return True, point_3d