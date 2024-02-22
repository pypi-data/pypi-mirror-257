import kognic.io.model as IAM
from examples.calibration.calibration import create_sensor_calibration
from kognic.io.client import KognicIOClient


def run(client: KognicIOClient, calibration_identifier: str) -> IAM.SensorCalibrationEntry:
    print("Listing Calibration...")

    lidar_sensor1 = "lidar"
    cam_sensors = [f"RFC0{i}" for i in range(1, 9)]

    # Create calibration
    calibration_spec = create_sensor_calibration(calibration_identifier, [lidar_sensor1], cam_sensors)
    created_calibration = client.calibration.create_calibration(calibration_spec)

    return created_calibration


if __name__ == "__main__":
    from datetime import datetime

    client = KognicIOClient()
    calibration_identifier = f"calibration-{datetime.now()}"
    run(client, calibration_identifier)
