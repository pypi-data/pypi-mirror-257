from __future__ import annotations

import torchvision.models as tv_models

from qai_hub_models.models._shared.imagenet_classifier.model import ImagenetClassifier

MODEL_ID = __name__.split(".")[-2]
DEFAULT_WEIGHTS = "IMAGENET1K_V2"


class MobileNetV2TV(ImagenetClassifier):
    model_builder = tv_models.mobilenet_v2
    DEFAULT_WEIGHTS = DEFAULT_WEIGHTS
