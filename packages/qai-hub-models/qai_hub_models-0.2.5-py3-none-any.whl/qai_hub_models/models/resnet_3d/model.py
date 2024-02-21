from __future__ import annotations

from typing import Any

import torchvision.models as tv_models

from qai_hub_models.models._shared.video_classifier.model import KineticsClassifier

MODEL_ID = __name__.split(".")[-2]
MODEL_ASSET_VERSION = "1"
DEFAULT_WEIGHTS: Any = tv_models.video.R3D_18_Weights.DEFAULT


class ResNet3D(KineticsClassifier):
    @staticmethod
    def from_pretrained(
        weights: Any = DEFAULT_WEIGHTS,
    ) -> KineticsClassifier:
        net = tv_models.video.r3d_18(weights=weights)
        return ResNet3D(net)
