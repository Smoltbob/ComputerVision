""""
Simple struct class for containing camera calibration
and exporting it.
"""

from dataclasses import dataclass, fields
import json

# TODO
# Specify our coordinate system
# Specify and justify our representations


@dataclass
class CameraCalibration:
    camera_name: str
    extrinsic_rotation: list
    extrinsic_translation: list

    def from_json(path):
        # Check that file exists and is correct
        with open(path) as f:
            json_data = json.loads(f)

        # Check that the fields are correct
        for expected_field in fields(CameraCalibration):
            assert (
                expect_field in json_data.keys()
            ), f"{expected_field} missing for calibration json"

        return CameraCalibration(
            camera_name=json_data["camera_name"],
            extrinsic_rotation=json_data["extrinsic_rotation"],
        )
