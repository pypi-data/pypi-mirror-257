from __future__ import absolute_import

from datetime import datetime
from typing import Optional
from uuid import uuid4

import kognic.io.model.scene as SceneModel
import kognic.io.model.scene.lidars_and_cameras_sequence as LidarsCamerasSequenceModel
from examples.calibration.calibration import create_sensor_calibration
from kognic.io.client import KognicIOClient
from kognic.io.logger import setup_logging
from kognic.io.model.scene.metadata.metadata import MetaData
from kognic.io.model.scene.resources import Image, PointCloud


def run(
    client: KognicIOClient,
    project: Optional[str],
    dryrun: bool = True,
) -> Optional[SceneModel.CreateSceneResponse]:

    print("Creating Lidar and Camera Sequence Scene...")

    lidar_sensor1 = "lidar"
    cam_sensor1 = "RFC01"
    cam_sensor2 = "RFC02"
    metadata = MetaData(
        **{
            "location-lat": 27.986065,
            "location-long": 86.922623,
            "vehicle_id": "abg",
        }
    )

    # Create calibration
    # (Please refer to the API documentation about calibration for more details)
    calibration_spec = create_sensor_calibration(
        f"Collection {datetime.now()}",
        [lidar_sensor1],
        [cam_sensor1, cam_sensor2],
    )
    created_calibration = client.calibration.create_calibration(calibration_spec)

    lidars_and_cameras_seq = LidarsCamerasSequenceModel.LidarsAndCamerasSequence(
        external_id=f"LCS-example-{uuid4()}",
        frames=[
            LidarsCamerasSequenceModel.Frame(
                frame_id="1",
                relative_timestamp=0,
                point_clouds=[
                    PointCloud(
                        filename="./examples/resources/point_cloud_RFL01.las",
                        sensor_name=lidar_sensor1,
                    ),
                ],
                images=[
                    Image(
                        filename="./examples/resources/img_RFC01.jpg",
                        sensor_name=cam_sensor1,
                    ),
                    Image(
                        filename="./examples/resources/img_RFC02.jpg",
                        sensor_name=cam_sensor2,
                    ),
                ],
                metadata={"dut_status": "active"},
            ),
            LidarsCamerasSequenceModel.Frame(
                frame_id="2",
                relative_timestamp=100,
                point_clouds=[
                    PointCloud(
                        filename="./examples/resources/point_cloud_RFL02.las",
                        sensor_name=lidar_sensor1,
                    ),
                ],
                images=[
                    Image(
                        filename="./examples/resources/img_RFC11.jpg",
                        sensor_name=cam_sensor1,
                    ),
                    Image(
                        filename="./examples/resources/img_RFC12.jpg",
                        sensor_name=cam_sensor2,
                    ),
                ],
                metadata={"dut_status": "active"},
            ),
        ],
        calibration_id=created_calibration.id,
        metadata=metadata,
    )
    # Add input
    input = client.lidars_and_cameras_sequence.create(
        lidars_and_cameras_seq,
        project=project,
        dryrun=dryrun,
    )
    return input


if __name__ == "__main__":
    setup_logging(level="INFO")
    client = KognicIOClient()

    # Project - Available via `client.project.get_projects()`
    project = "<project-identifier>"
    run(client, project)
