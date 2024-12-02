import logging
from abc import ABC
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from tqdm import tqdm

import cv2
import numpy as np

from superglue_lib.models.utils import process_resize
from svl.keypoint_pipeline.typing import ImageKeyPoints
from svl.keypoint_pipeline.base import CombinedKeyPointAlgorithm

@dataclass
class BaseMapReaderItem:
    image_path: Path
    image: Optional[np.ndarray] = None
    size: Optional[Tuple[int, int]] = None
    key_points: Optional[ImageKeyPoints] = None
    name: str = field(init=False)


class BaseMapReader(ABC):
    """Base class for reading and processing map images

    Parameters
    ----------
    logger : logging.Logger
        Logger object
    resize_size : Optional[Tuple[int, int]], optional
        Size to resize the images to, by default None
    cv2_read_mode : int, optional
        OpenCV read mode, by default cv2.IMREAD_COLOR

    """

    IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]

    def __init__(
        self,
        db_path: Path,
        logger: logging.Logger,
        resize_size: Optional[Tuple[int, int]] = None,
        cv2_read_mode: int = cv2.IMREAD_COLOR,
    ) -> None:
        db_path = db_path if isinstance(db_path, Path) else Path(db_path)
        if not db_path.exists():
            raise FileNotFoundError(f"Database path not found at {db_path}")
        if not db_path.is_dir():
            raise NotADirectoryError(f"Database path is not a directory at {db_path}")
        self.db_path = db_path
        self.cv2_read_mode = cv2_read_mode
        self.resize_size = resize_size
        self.logger = logger
        self._initialize_db()

    def _initialize_db(self) -> None:
        """Initialize the image database"""
        self._image_db: List[BaseMapReaderItem] = []
        self._num_images: int = 0
        self._is_loaded: bool = False
        self._is_described: bool = False

    @property
    def image_names(self) -> List[str]:
        """List of image names in the database"""
        return [image.name for image in self._image_db]

    def __len__(self) -> int:
        """Number of images in the database"""
        return self._num_images

    def __getitem__(self, key: Union[int, str]) -> BaseMapReaderItem:
        """Get image item from the database

        Parameters
        ----------
        key : Union[int, str]
            Index or name of the image. If key is an integer, it returns the image at
            that index. If key is a string, it returns the image with that name.

        Returns
        -------
        BaseMapReaderItem
            Image item from the database
        """
        if isinstance(key, int):
            if key < 0 or key >= len(self._image_db):
                raise IndexError("Index out of range")
            return self._image_db[key]
        elif isinstance(key, str):
            if key not in self.image_names:
                raise KeyError(f"Image with name {key} not found in the database")
            for img_item in self._image_db:
                if img_item.name == key:
                    return img_item
        else:
            raise KeyError("Key must be either an integer or a string")

    def read(self, image_path: Union[str, Path]) -> np.ndarray:
        """Read image from file

        Parameters
        ----------
        image_path : Union[str, Path]
            Path to the image file

        Returns
        -------
        np.ndarray
            Image array
        """
        image_path = image_path if isinstance(image_path, Path) else Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found at {image_path}")

        img = cv2.imread(str(image_path), self.cv2_read_mode)

        return img

    def load_images(self) -> None:
        """Load images from the database"""

        if self._is_loaded:
            self.logger.info("Images already loaded")
            return
        for idx in tqdm(range(len(self)), desc="Loading images", total=len(self)):
            self[idx].image = self.read(self[idx].image_path)
            self[idx].size = self[idx].image.shape[:2]
        self._is_loaded = True
        self.logger.info("Images loaded successfully")

    def resize(self, image: np.ndarray) -> np.ndarray:
        """Resize image given np.ndarray. It first computes the new size based on the
        resize_size attribute and then resizes the image.

        Parameters
        ----------
        image : np.ndarray
            Image array, shape (height, width, channels)

        Returns
        -------
        np.ndarray
            Resized image array
        """
        if self.resize_size is None:
            return image
        height, width = image.shape[:2]
        new_width, new_height = process_resize(width, height, self.resize_size)
        resized_image = cv2.resize(
            image, (new_width, new_height), interpolation=cv2.INTER_AREA
        )
        return resized_image

    def resize_image(self, image_name: str) -> None:
        """Resize image item in the database

        Parameters
        ----------
        image_name : str
            Name of the image to resize
        """
        if self[image_name].image is None:
            self.logger.info(f"Image {image_name} not loaded. Loading image")
            self[image_name].image = self.read(self[image_name].image_path)

        img_item = self[image_name]
        img_item.image = self.resize(img_item.image)
        img_item.size = img_item.image.shape[:2]

    def resize_db_images(self) -> None:
        """Resize all images in the database"""
        self.logger.info("Resizing images in the database")
        for imge_name in tqdm(self.image_names):
            self.resize_image(imge_name)

    def extract_features(
        self, image: np.ndarray, algorithm: CombinedKeyPointAlgorithm
    ) -> ImageKeyPoints:
        """Extract features from an image using the given algorithm

        Parameters
        ----------
        image : np.ndarray
            Image array to extract features from
        algorithm : CombinedKeyPointAlgorithm
            Key point detection and description algorithm
        """
        return algorithm.detect_and_describe_keypoints(image)

    def extract_features_from_image(
        self, image_name: str, algorithm: CombinedKeyPointAlgorithm
    ) -> None:
        """Extract features from an image in the database using the given algorithm

        Parameters
        ----------
        image_name : str
            Name of the image to extract features from
        algorithm : CombinedKeyPointAlgorithm
            Key point detection and description algorithm
        """
        kp: ImageKeyPoints = self.extract_features(self[image_name].image, algorithm)
        self[image_name].key_points = kp

    def describe_db_images(self, algorithm: CombinedKeyPointAlgorithm) -> None:
        """Describe all images in the database using the given algorithm

        Parameters
        ----------
        algorithm : CombinedKeyPointAlgorithm
            Key point detection and description algorithm
        """

        if not self._is_loaded:
            raise ValueError("Images are not loaded, call load_images() first")
        self.logger.info(
            f"Describing images in the database using {algorithm.__class__.__name__}"
        )
        for img_info in tqdm(self._image_db):
            self.extract_features_from_image(img_info.name, algorithm)

        self._is_described = True