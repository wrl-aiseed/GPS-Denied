import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

from svl.localization.base import BaseMapReader
from svl.tms.data_structures import (
    FlightZone,
    GeoSatelliteImage,
    Mosaic,
    Tile,
    TileImage,
)
from svl.tms.schemas import GpsCoordinate

class SatelliteMapReader(BaseMapReader):
    """Class for reading and processing satellite map images

    This class reads satellite map images and their metadata from a directory.
    The metadata is expected to be in a CSV file with the columns specified in the
    `COLUMN_NAMES` attribute.


    Parameters
    ----------
    db_path : Path
        Path to the directory containing the images
    logger : logging.Logger
        Logger object
    resize_size : Tuple[int, int]
        Size to resize the images to
    cv2_read_mode : int, optional
        OpenCV read mode, by default cv2.IMREAD_GRAYSCALE
    metadata_method : str, optional
        Method to load metadata, by default "CSV"
    """

    COLUMN_NAMES = [
        "Filename",
        "Top_left_lat",
        "Top_left_lon",
        "Bottom_right_lat",
        "Bottom_right_long",
    ]
    METADATA_METHOD = [
        "CSV",
    ]

    def __init__(
        self,
        db_path: Path,
        logger: logging.Logger,
        resize_size: Tuple[int, int],
        cv2_read_mode: int = cv2.IMREAD_GRAYSCALE,
        metadata_method: str = "CSV",
    ) -> None:
        super().__init__(db_path, logger, resize_size, cv2_read_mode)
        if metadata_method not in self.METADATA_METHOD:
            raise ValueError(f"Invalid metadata method {metadata_method}")

    def setup_db(self) -> None:
        """Setup the image database."""
        self._build_image_db()
        self.load_images()
        self._load_csv_metadata()
        self.set_metadata_for_all_images()

    def initialize_db(self) -> None:
        """Initialize the image database."""
        super()._initialize_db()
        self._geo_metadata: pd.DataFrame = None

    def _build_image_db(self) -> None:
        """Build the image database from the images in the directory."""
        self.logger.info(f"Building image database from {self.db_path}: ")
        img_idx = 0
        for image_path in tqdm(sorted(self.db_path.glob("*"))):
            if image_path.suffix in self.IMAGE_EXTENSIONS:
                self._image_db.append(
                    GeoSatelliteImage(
                        image_path=image_path,
                        index=img_idx,
                    )
                )
                img_idx += 1

        self._num_images = img_idx
        self.logger.info(
            f"Image database built successfully with {self._num_images} images"
        )

    def _load_csv_metadata(self):
        """Load metadata from a CSV file into a DataFrame."""
        csv_files = list(self.db_path.glob("*.csv"))
        if len(csv_files) == 0:
            raise FileNotFoundError(f"No CSV files found in {self.db_path}")
        if len(csv_files) > 1:
            raise ValueError(f"Multiple CSV files found in {self.db_path}")
        csv_file = csv_files[0]
        self.logger.info(f"Loading metadata from {csv_file}")
        df = pd.read_csv(csv_file)
        if not all(col in df.columns for col in self.COLUMN_NAMES):
            raise ValueError(f"Invalid metadata columns in {csv_file}")
        df["Filename"] = df["Filename"].apply(lambda x: x.split(".")[0])
        self._geo_metadata = df
        self.logger.info("Metadata loaded successfully")

    def set_image_metadata(self, image_name: str, metadata: Dict[str, float]) -> None:
        """Set metadata for a specific image."""
        satellite_image: GeoSatelliteImage = self[image_name]
        satellite_image.top_left = GpsCoordinate(
            lat=metadata["Top_left_lat"], long=metadata["Top_left_lon"]
        )
        satellite_image.bottom_right = GpsCoordinate(
            lat=metadata["Bottom_right_lat"], long=metadata["Bottom_right_long"]
        )

    def set_metadata_for_all_images(self) -> None:
        """Set metadata for all images in the database."""
        self.logger.info("Setting metadata for all images")

        for img_info in tqdm(self._image_db):
            img_metadata = self._geo_metadata[
                self._geo_metadata["Filename"] == img_info.name
            ]
            if len(img_metadata) == 1:
                img_metadata = img_metadata.to_dict(orient="records")[0]
                del img_metadata["Filename"]
                self.set_image_metadata(img_info.name, img_metadata)
            elif len(img_metadata) > 1:
                self.logger.warning(
                    f"Multiple metadata entries found for image {img_info.name}"
                )
            else:
                self.logger.warning(f"Metadata not found for image {img_info.name}")

    @property
    def goe_metadata(self) -> pd.DataFrame:
        return self._geo_metadata
