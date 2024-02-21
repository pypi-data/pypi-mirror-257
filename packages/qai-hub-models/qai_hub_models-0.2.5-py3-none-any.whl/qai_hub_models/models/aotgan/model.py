from __future__ import annotations

import torch
import torch.nn as nn

from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, SourceAsRoot
from qai_hub_models.utils.base_model import BaseModel
from qai_hub_models.utils.input_spec import InputSpec

AOTGAN_SOURCE_REPOSITORY = "https://github.com/researchmm/AOT-GAN-for-Inpainting/"
AOTGAN_SOURCE_REPO_COMMIT = "418034627392289bdfc118d62bc49e6abd3bb185"
MODEL_ID = __name__.split(".")[-2]
SUPPORTED_PRETRAINED_MODELS = set(["celebahq", "places2"])
DEFAULT_WEIGHTS = "celebahq"
MODEL_ASSET_VERSION = 1


class AOTGAN(BaseModel):
    """Exportable AOTGAN for Image inpainting"""

    def __init__(self, model: nn.Module) -> None:
        super().__init__()
        self.model = model

    @classmethod
    def from_pretrained(cls, ckpt_name: str = DEFAULT_WEIGHTS):
        if ckpt_name not in SUPPORTED_PRETRAINED_MODELS:
            raise ValueError(
                "Unsupported pre_trained model requested. Please provide either 'celeabhq' or 'places2'."
            )
        downloaded_model_path = CachedWebModelAsset.from_asset_store(
            MODEL_ID,
            MODEL_ASSET_VERSION,
            f"pretrained_models/{ckpt_name}/G0000000.pt",
        ).fetch()
        with SourceAsRoot(
            AOTGAN_SOURCE_REPOSITORY,
            AOTGAN_SOURCE_REPO_COMMIT,
            MODEL_ID,
            MODEL_ASSET_VERSION,
        ):
            from src.model.aotgan import InpaintGenerator

            # AOT-GAN InpaintGenerator uses ArgParser to
            # initialize model and it uses following two parameters
            #  - rates: default value [1, 2, 4, 8]
            #  - block_num: default value 8
            # creating dummy class with default values to set the same
            class InpaintArgs:
                def __init__(self):
                    self.rates = [1, 2, 4, 8]
                    self.block_num = 8

            args = InpaintArgs()
            model = InpaintGenerator(args)
            model.load_state_dict(torch.load(downloaded_model_path, map_location="cpu"))
            return cls(model)

    def forward(self, image: torch.Tensor, mask: torch.Tensor):
        """
        Run AOTGAN Inpaint Generator on `image` with given `mask`
        and generates new high-resolution in-painted image.

        Parameters:
            image: Pixel values pre-processed of shape [N, C, H, W]
                    Range: float[0, 1]
                    3-channel color Space: BGR
            mask: Pixel values pre-processed to have have mask values either 0. or 1.
                    Range: float[0, 1] and only values of 0. or 1.
                    1-channel binary image.

        Returns:
            In-painted image for given image and mask of shape [N, C, H, W]
            Range: float[0, 1]
            3-channel color space: RGB
        """
        return self.model(image, mask)

    def get_input_spec(
        self,
        batch_size: int = 1,
        num_channels: int = 3,
        height: int = 512,
        width: int = 512,
    ) -> InputSpec:
        """
        Returns the input specification (name -> (shape, type). This can be
        used to submit profiling job on Qualcomm AI Hub.
        """
        return {
            "image": ((batch_size, num_channels, height, width), "float32"),
            "mask": ((batch_size, 1, height, width), "float32"),
        }
