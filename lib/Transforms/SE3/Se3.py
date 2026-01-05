import numpy as np
from lib.Math.rotation_utils import euler_to_rot_mat

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