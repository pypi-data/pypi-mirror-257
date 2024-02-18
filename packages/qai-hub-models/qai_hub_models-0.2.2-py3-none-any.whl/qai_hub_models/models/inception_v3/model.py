from __future__ import annotations

import torchvision.models as tv_models

from qai_hub_models.models._shared.imagenet_classifier.model import ImagenetClassifier

MODEL_ID = __name__.split(".")[-2]
DEFAULT_WEIGHTS = "IMAGENET1K_V1"


class InceptionNetV3(ImagenetClassifier):
    model_builder = tv_models.inception_v3
    DEFAULT_WEIGHTS = DEFAULT_WEIGHTS
