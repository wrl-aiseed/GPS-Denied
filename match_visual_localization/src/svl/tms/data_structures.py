from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Generator, List, Tuple, Union
import math

import numpy as np

from svl.keypoint_pipeline.typing import ImageKeyPoints
from svl.tms.schemas import GpsCoordinate
from svl.utils.io import JsonParser, YamlParser


@dataclass
class GeoSatelliteImage:
    """A GeoSatelliteImage is a dataclass that represents an image captured by a satellite.

    Parameters
    ----------
    image_path : Path
        path to the image file
    top_left : GpsCoordinate
        top left corner of the image (latitude, longitude)
    bottom_right : GpsCoordinate
        bottom right corner of the image (latitude, longitude)
    image : np.ndarray
        image as a numpy array
    key_points : ImageKeyPoints
        key points of the image

    Properties
    ----------
    name : str
        name of the image (file name without extension)
    """

    image_path: Path
    top_left: GpsCoordinate = None
    bottom_right: GpsCoordinate = None
    image: np.ndarray = None
    index: int = None
    key_points: ImageKeyPoints = None
    name: str = field(init=False)

    def __post_init__(self):
        self.name = self.image_path.stem



@dataclass
class CameraModel:
    """A CameraModel is a dataclass that represents the intrinsic parameters of a camera.

    Parameters
    ----------
    focal_length : float
        focal length of the camera in millimeters
    resolution_width : int
        width of the image in pixels
    resolution_height : int
        height of the image in pixels
    hfov_deg : float
        horizontal field of view in degrees
    principal_point_x : float
        x coordinate of the principal point
    principal_point_y : float
        y coordinate of the principal point

    Properties
    ----------
    hfov_rad : float
        horizontal field of view in radians
    resolution : Tuple
        resolution of the image
    aspect_ratio : float
        aspect ratio of the image
    focal_length_px : float
        focal length in pixels
    """

    focal_length: float
    resolution_width: int
    resolution_height: int
    hfov_deg: float
    hfov_rad: float = field(init=False)
    resolution: Tuple = field(init=False)
    aspect_ratio: float = field(init=False)
    focal_length_px: float = field(init=False)
    principal_point_x: float = None
    principal_point_y: float = None

    def __post_init__(self) -> None:
        self.hfov_rad = self.hfov_deg * (math.pi / 180)
        self.resolution = (self.resolution_width, self.resolution_height)
        self.aspect_ratio = self.resolution_width / self.resolution_height
        self.focal_length_px = self.resolution_width / (2 * math.tan(self.hfov_rad / 2))
        if self.principal_point_x is None:
            self.principal_point_x = self.resolution_width / 2
        if self.principal_point_y is None:
            self.principal_point_y = self.resolution_height / 2

    @staticmethod
    def from_yaml(yaml_file: str) -> CameraModel:
        data = YamlParser.load_yaml(yaml_file)
        return CameraModel(
            focal_length=data["focal_length"],
            resolution_width=data["resolution_width"],
            resolution_height=data["resolution_height"],
            hfov_deg=data["hfov_deg"],
        )

    @staticmethod
    def from_json(json_file: str) -> CameraModel:
        data = JsonParser.load_json(json_file)
        return CameraModel(
            focal_length=data["focal_length"],
            resolution_width=data["resolution_width"],
            resolution_height=data["resolution_height"],
            hfov_deg=data["hfov_deg"],
        )