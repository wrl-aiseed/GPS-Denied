from abc import ABC, abstractmethod

import numpy as np

from svl.keypoint_pipeline.typing import ImageKeyPoints

class CombinedKeyPointAlgorithm(ABC):
    """Abstract class for combined keypoint detection and description."""

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def detect_keypoints(self, image: np.ndarray) -> np.ndarray:
        """
        Detect keypoints in an image.

        Parameters
        ----------
        image : np.ndarray
            image to detect keypoints in

        Returns
        -------
        np.ndarray
            keypoints
        """
        pass

    @abstractmethod
    def describe_keypoints(self, image: np.ndarray, keypoints: np.ndarray) -> np.ndarray:
        """
        Describe keypoints in an image.

        Parameters
        ----------
        image : np.ndarray
            image to describe keypoints in
        keypoints : np.ndarray
            keypoints to describe

        Returns
        -------
        np.ndarray
            descriptors
        """
        pass

    @abstractmethod
    def detect_and_describe_keypoints(self, image: np.ndarray) -> ImageKeyPoints:
        """
        Detect and describe keypoints in an image.

        Parameters
        ----------
        image : np.ndarray
            image to detect and describe keypoints in

        Returns
        -------
        ImageKeyPoints
            keypoints and descriptors
        """
        pass