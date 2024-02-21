from __future__ import annotations

import torch

from qai_hub_models.evaluators.base_evaluators import BaseEvaluator
from qai_hub_models.models._shared.deeplab.evaluator import DeepLabV3Evaluator
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, SourceAsRoot
from qai_hub_models.utils.base_model import BaseModel
from qai_hub_models.utils.input_spec import InputSpec

MODEL_ID = __name__.split(".")[-2]
MODEL_ASSET_VERSION = 1
# Weights downloaded from https://github.com/quic/aimet-model-zoo/releases/download/phase_2_january_artifacts/deeplab-mobilenet.pth.tar
DEEPLABV3_WEIGHTS = "deeplab-mobilenet.pth.tar"
DEEPLABV3_SOURCE_REPOSITORY = "https://github.com/jfzhang95/pytorch-deeplab-xception"
DEEPLABV3_SOURCE_REPO_COMMIT = "9135e104a7a51ea9effa9c6676a2fcffe6a6a2e6"
BACKBONE = "mobilenet"
NUM_CLASSES = 21


class DeepLabV3PlusMobilenet(BaseModel):
    """Exportable DeepLabV3_Plus_MobileNet image segmentation applications, end-to-end."""

    def __init__(
        self,
        deeplabv3_model: torch.nn.Module,
    ) -> None:
        super().__init__()
        self.model = deeplabv3_model

    @classmethod
    def from_pretrained(cls) -> DeepLabV3PlusMobilenet:
        model = _load_deeplabv3_source_model()
        dst = CachedWebModelAsset.from_asset_store(
            MODEL_ID, MODEL_ASSET_VERSION, DEEPLABV3_WEIGHTS
        ).fetch()
        checkpoint = torch.load(dst, map_location=torch.device("cpu"))
        model.load_state_dict(checkpoint["state_dict"])
        model.eval()

        return cls(model)

    def get_evaluator(self) -> BaseEvaluator:
        return DeepLabV3Evaluator(NUM_CLASSES)

    def forward(self, image: torch.Tensor) -> torch.Tensor:
        """
        Run DeepLabV3_Plus_Mobilenet on `image`, and produce a tensor of classes for segmentation

        Parameters:
            image: Pixel values pre-processed for model consumption.
                   Range: float[0, 1]
                   3-channel Color Space: RGB

        Returns:
            tensor: Bx21xHxW tensor of class logits per pixel
        """
        return self.model(image)

    @staticmethod
    def get_input_spec(
        batch_size: int = 1,
        num_channels: int = 3,
        height: int = 224,
        width: int = 224,
    ) -> InputSpec:
        # Get the input specification ordered (name -> (shape, type)) pairs for this model.
        #
        # This can be used with the qai_hub python API to declare
        # the model input specification upon submitting a profile job.
        return {"image": ((batch_size, num_channels, height, width), "float32")}


def _load_deeplabv3_source_model() -> torch.nn.Module:
    # Load DeepLabV3 model from the source repository using the given weights.
    # Returns <source repository>.modeling.deeplab.DeepLab
    with SourceAsRoot(
        DEEPLABV3_SOURCE_REPOSITORY,
        DEEPLABV3_SOURCE_REPO_COMMIT,
        MODEL_ID,
        MODEL_ASSET_VERSION,
    ):
        # necessary import. `modeling.deeplab` comes from the DeepLabV3 repo.
        from modeling.deeplab import DeepLab

        return DeepLab(backbone=BACKBONE, sync_bn=False, num_classes=NUM_CLASSES)
