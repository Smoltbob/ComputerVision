import numpy as np
from lib.Math.rotation_utils import euler_to_rot_mat
from typing import List

class Se3:
    def __init__(self, translation: np.ndarray, rotation: np.ndarray):
        self.translation = translation
        self.rotation = rotation

    def __mul__(self, other: "Se3") -> "Se3":
        new_translation = self.rotation @ other.translation + self.translation
        new_rotation = self.rotation @ other.rotation
        return Se3(new_translation, new_rotation)
    
    def getMatrix3x4(self) -> np.ndarray:
        """Returns the 3x4 transformation matrix."""
        mat = np.zeros((3, 4))
        mat[:, :3] = self.rotation
        mat[:, 3] = self.translation
        return mat
    
    def getMatrix4x4(self) -> np.ndarray:
        """Returns the 4x4 transformation matrix."""
        mat = np.eye(4)
        mat[:3, :3] = self.rotation
        mat[:3, 3] = self.translation
        return mat
    
    def getAxisAngle(self) -> List[float]:
        """
        Converts the rotation matrix to axis-angle representation.
        Returns a list of 3 floats representing the rotation vector.
        """
        angle = np.arccos((np.trace(self.rotation) - 1) / 2)
        if np.isclose(angle, 0):
            return np.array([0.0, 0.0, 0.0])
        rx = self.rotation[2, 1] - self.rotation[1, 2]
        ry = self.rotation[0, 2] - self.rotation[2, 0]
        rz = self.rotation[1, 0] - self.rotation[0, 1]
        r = np.array([rx, ry, rz])
        r = (angle / (2 * np.sin(angle))) * r
        return r
    
    def getTranslation(self) -> List[float]:
        """Returns the translation vector as a list of 3 floats."""
        return self.translation
    
    def transformPoint(self, point: np.ndarray) -> np.ndarray:
        """
        Transforms a 3D point using the SE3 transformation,
        doing A * point if A = self.getMatrix4x4()

        Args:
            point: An homogeneous 3D point as a numpy array of shape (4,)
        """
        point1 = self.rotation @ point[:3] + point[3] * self.translation
        return np.array([*point1, point[3]])

    @staticmethod
    def from_euler_angles(translation: np.ndarray, roll: float, pitch: float, yaw: float) -> "Se3":
        """
        Create a Se3 object from translation and Euler angles (roll, pitch, yaw).
        Angles are in radians.
        """
        rotation = euler_to_rot_mat(roll, pitch, yaw)
        return Se3(translation, rotation)
    
    def inverse(self) -> "Se3":
        inv_rotation = self.rotation.T
        inv_translation = -inv_rotation @ self.translation
        return Se3(inv_translation, inv_rotation)