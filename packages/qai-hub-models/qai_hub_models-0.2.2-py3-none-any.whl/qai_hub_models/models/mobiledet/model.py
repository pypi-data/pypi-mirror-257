from __future__ import annotations

import torch

from qai_hub_models.utils.asset_loaders import SourceAsRoot
from qai_hub_models.utils.base_model import BaseModel
from qai_hub_models.utils.input_spec import InputSpec

MOBILEDET_SOURCE_REPOSITORY = "https://github.com/novice03/mobiledet-pytorch"
MOBILEDET_SOURCE_REPO_COMMIT = "f8af166187f82b3356e023185edebdfdb2a3aa6b"
MODEL_ID = __name__.split(".")[-2]
DEFAULT_WEIGHTS = "dsp"
MODEL_ASSET_VERSION = 1


class MobileDet(BaseModel):
    """Exportable MobileDet backbone"""

    def __init__(
        self,
        model: torch.nn.Module,
    ) -> None:
        super().__init__()
        self.model = model

    @classmethod
    def from_pretrained(
        cls,
        backbone_type: str = DEFAULT_WEIGHTS,
    ) -> MobileDet:
        """Load MobileDet from a weightfile created by the source MobileDet repository."""

        # Load PyTorch model from disk
        model = _load_mobiledet_source_model_from_backbone(backbone_type)

        return MobileDet(model)

    def forward(self, image: torch.Tensor) -> torch.Tensor:
        """
        Run MobileDet on `image`, and produce an upscaled image

        Parameters:
            image: Pixel values pre-processed for GAN consumption.
                   Range: float[0, 1]
                   3-channel Color Space: RGB

        Returns:
            image: Pixel values
                   Range: float[0, 1]
                   3-channel Color Space: RGB
        """
        return self.model(image)

    def get_input_spec(
        self,
        batch_size: int = 1,
        num_channels: int = 3,
        height: int = 640,
        width: int = 640,
    ) -> InputSpec:
        # Get the input specification ordered (name -> (shape, type)) pairs for this model.
        #
        # This can be used with the qai_hub python API to declare
        # the model input specification upon submitting a profile job.
        return {"image": ((batch_size, num_channels, height, width), "float32")}


def _load_mobiledet_source_model_from_backbone(
    backbone_type: str,
) -> torch.nn.Module:
    with SourceAsRoot(
        MOBILEDET_SOURCE_REPOSITORY,
        MOBILEDET_SOURCE_REPO_COMMIT,
        MODEL_ID,
        MODEL_ASSET_VERSION,
    ):
        # Fix import issues in the repo. Each of the following
        # files needs to import torch.nn
        with open("mobiledet_dsp.py", "r") as file:
            dsp_content = file.read()
        new_content = "import torch.nn as nn\n" + dsp_content
        with open("mobiledet_dsp.py", "w") as file:
            file.write(new_content)

        with open("mobiledet_gpu.py", "r") as file:
            gpu_content = file.read()
        new_content = "import torch.nn as nn\n" + gpu_content
        with open("mobiledet_gpu.py", "w") as file:
            file.write(new_content)

        with open("mobiledet_tpu.py", "r") as file:
            tpu_content = file.read()
        new_content = "import torch.nn as nn\n" + tpu_content
        with open("mobiledet_tpu.py", "w") as file:
            file.write(new_content)

        from mobiledet_dsp import MobileDetDSP
        from mobiledet_gpu import MobileDetGPU
        from mobiledet_tpu import MobileDetTPU

        if backbone_type == "dsp":
            model = MobileDetDSP()
        elif backbone_type == "gpu":
            model = MobileDetGPU()
        elif backbone_type == "tpu":
            model = MobileDetTPU()
        else:
            raise ValueError(
                f"Incorrect backbone_type({backbone_type}) specificed."
                " Provide one of 'dsp', 'gpu' or 'tpu'."
            )

        model.eval()
        return model
