import dataclasses

import numpy as np
import torch

from superglue_lib.models.superpoint import SuperPoint
from superglue_lib.models.utils import frame2tensor

from svl.keypoint_pipeline.typing import ImageKeyPoints, SuperPointConfig
from svl.keypoint_pipeline.base import (
    CombinedKeyPointAlgorithm,
    KeyPointDescriptor,
    KeyPointDetector,
)

@CombinedKeyPointAlgorithm.register
class SuperPointAlgorithm(CombinedKeyPointAlgorithm):
    """SuperPoint Keypoint Algorithm that can be used to detect and describe keypoints.

    Parameters
    ----------
    config : SuperPointConfig
        configuration for SuperPoint
    """

    def __init__(self, config: SuperPointConfig) -> None:
        super().__init__()
        self.config = config
        self.detector = SuperPoint(dataclasses.asdict(config))
        self.detector = self.detector.eval()
        self.detector = self.detector.to(config.device)

    def detect_and_describe_keypoints(self, image: np.ndarray) -> ImageKeyPoints:
        """
        Detect keypoints in an image using SuperPoint.

        Parameters
        ----------
        image : np.ndarray
            image to detect keypoints in

        Returns
        -------
        ImageKeyPoints
            keypoints with their descriptors
        """

        tensor = frame2tensor(image, self.config.device)
        data = {
            "image": tensor,
        }
        with torch.no_grad():
            outputs = self.detector(data)
        outputs = {k: v[0] for k, v in outputs.items()}
        outputs["descriptors"] = outputs["descriptors"].transpose(1, 0)
        outputs["image_size"] = [image.shape[0], image.shape[1]]
        outputs = ImageKeyPoints(**outputs).to("cpu").numpy()
        return outputs

    def detect_keypoints(self, image: np.ndarray) -> np.ndarray:
        """
        Detect keypoints in an image using SuperPoint.

        Parameters
        ----------
        image : np.ndarray
            image to detect keypoints in

        Returns
        -------
        np.ndarray
            keypoints
        """
        tensor = frame2tensor(image, self.config.device)
        data = {
            "image": tensor,
        }
        with torch.no_grad():
            outputs = self.detector(data)
        outputs = {k: v[0] for k, v in outputs.items()}
        outputs["descriptors"] = outputs["descriptors"].transpose(1, 0)
        outputs["image_size"] = [image.shape[0], image.shape[1]]
        outputs = ImageKeyPoints(**outputs).to("cpu").numpy()
        return outputs.keypoints

    def describe_keypoints(self, image: np.ndarray, keypoints: np.ndarray) -> np.ndarray:
        raise NotImplementedError("SuperPoint does not support describing keypoints.")
