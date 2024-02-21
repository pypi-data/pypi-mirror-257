from __future__ import annotations

import torch
from aimet_torch.cross_layer_equalization import equalize_model
from aimet_torch.quantsim import QuantizationSimModel, load_encodings_to_sim

from qai_hub_models.models.deeplabv3_plus_mobilenet.model import (
    DeepLabV3PlusMobilenet,
    _load_deeplabv3_source_model,
)
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset

# This verifies aimet is installed, and this must be included first.
from qai_hub_models.utils.quantization_aimet import (  # isort: skip
    AIMETQuantizableMixin,
)


MODEL_ID = __name__.split(".")[-2]
MODEL_ASSET_VERSION = 1

# Note: Original model definition can be found at https://github.com/jfzhang95/pytorch-deeplab-xception
# The definition was pulled into the AIMET Model Zoo (the source of the below weights, encodings, and config).
QUANTIZED_WEIGHTS = "dlv3_w8a8_state_dict.pth"
AIMET_ENCODINGS = "aimet_quantization_encodings.json"
AIMET_CONFIG = "aimet_config.json"


class DeepLabV3PlusMobileNetQuantizable(AIMETQuantizableMixin, DeepLabV3PlusMobilenet):
    """
    DeepLabV3PlusMobileNet with post train quantization support.

    Supports only 8 bit weights and activations
    """

    def __init__(
        self,
        deeplabv3_model: QuantizationSimModel,
    ) -> None:
        DeepLabV3PlusMobilenet.__init__(self, deeplabv3_model.model)
        AIMETQuantizableMixin.__init__(
            self, deeplabv3_model, needs_onnx_direct_aimet_export=True
        )

    @classmethod
    def from_pretrained(cls) -> "DeepLabV3PlusMobileNetQuantizable":
        # Load Model
        deeplabv3 = _load_deeplabv3_source_model()
        input_shape = DeepLabV3PlusMobileNetQuantizable.get_input_spec()["image"][0]
        equalize_model(deeplabv3, input_shape)

        # Download weights and quantization parameters
        weights = CachedWebModelAsset.from_asset_store(
            MODEL_ID, MODEL_ASSET_VERSION, QUANTIZED_WEIGHTS
        ).fetch()
        aimet_config = CachedWebModelAsset.from_asset_store(
            MODEL_ID, MODEL_ASSET_VERSION, AIMET_CONFIG
        ).fetch()
        aimet_encodings = CachedWebModelAsset.from_asset_store(
            MODEL_ID, MODEL_ASSET_VERSION, AIMET_ENCODINGS
        ).fetch()

        # Load the model weights and quantization parameters
        state_dict = torch.load(weights, map_location=torch.device("cpu"))
        deeplabv3.load_state_dict(state_dict)
        sim = QuantizationSimModel(
            deeplabv3,
            quant_scheme="tf_enhanced",
            default_param_bw=8,
            default_output_bw=8,
            config_file=aimet_config,
            dummy_input=torch.rand(input_shape),
        )
        load_encodings_to_sim(sim, aimet_encodings)

        return cls(sim)
