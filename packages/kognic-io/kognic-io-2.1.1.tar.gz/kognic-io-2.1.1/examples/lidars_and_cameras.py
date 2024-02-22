from __future__ import absolute_import

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

import kognic.io.model.scene as SceneModel
import kognic.io.model.scene.lidars_and_cameras as LidarsCamerasModel
from examples.calibration.calibration import create_sensor_calibration
from kognic.io.client import KognicIOClient
from kognic.io.logger import setup_logging
from kognic.io.model.scene.metadata.metadata import MetaData
from kognic.io.model.scene.resources import Image, PointCloud


def run(
    client: KognicIOClient,
    project: Optional[str],
    annotation_types: Optional[List[str]] = None,
    dryrun: bool = True,
) -> SceneModel.CreateSceneResponse:

    annotation_types = annotation_types or []
    print("Creating Lidars And Cameras Scene...")

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

    lidars_and_cameras = LidarsCamerasModel.LidarsAndCameras(
        external_id=f"lidars-and-cameras-example-{uuid4()}",
        frame=LidarsCamerasModel.Frame(
            point_clouds=[
                PointCloud(
                    filename="./examples/resources/point_cloud_RFL01.las",
                    sensor_name=lidar_sensor1,
                )
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
        ),
        calibration_id=created_calibration.id,
        metadata=metadata,
    )

    # Create input
    input = client.lidars_and_cameras.create(
        lidars_and_cameras,
        project=project,
        annotation_types=annotation_types,
        dryrun=dryrun,
    )
    return input


if __name__ == "__main__":
    setup_logging(level="INFO")
    client = KognicIOClient()

    # Project - Available via `client.project.get_projects()`
    project = "<project-identifier>"
    # Annotation Types - Available via `client.project.get_annotation_types(project)`
    annotation_types = ["annotation-type"]

    run(client, project, annotation_types)
