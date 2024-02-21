import os
import tempfile
import zipfile

import numpy as np
import torch

from qai_hub_models.models._shared.deeplab.app import DeepLabV3App
from qai_hub_models.models.deeplabv3_plus_mobilenet.model import NUM_CLASSES
from qai_hub_models.models.deeplabv3_plus_mobilenet.test import INPUT_IMAGE_ADDRESS
from qai_hub_models.models.deeplabv3_plus_mobilenet_quantized.demo import (
    main as demo_main,
)
from qai_hub_models.models.deeplabv3_plus_mobilenet_quantized.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    DeepLabV3PlusMobileNetQuantizable,
)
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, load_image
from qai_hub_models.utils.testing import assert_most_close, skip_clone_repo_check

OUTPUT_IMAGE_LOCAL_PATH = "deeplabv3_quantized_demo_output.png"
OUTPUT_IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, OUTPUT_IMAGE_LOCAL_PATH
)


@skip_clone_repo_check
def test_task():
    # AIMET Quantization Simulator introduces randomness. Eliminate that for this test.
    torch.manual_seed(0)
    image = load_image(INPUT_IMAGE_ADDRESS)
    output_image = load_image(OUTPUT_IMAGE_ADDRESS)
    app = DeepLabV3App(
        DeepLabV3PlusMobileNetQuantizable.from_pretrained(), num_classes=NUM_CLASSES
    )
    app_output_image = app.predict(image, False)

    assert_most_close(
        np.asarray(app_output_image, dtype=np.float32) / 255,
        np.asarray(output_image, dtype=np.float32) / 255,
        diff_tol=0.005,
        rtol=0.02,
        atol=0.2,
    )


@skip_clone_repo_check
def test_trace():
    image = load_image(INPUT_IMAGE_ADDRESS)
    output_image = load_image(OUTPUT_IMAGE_ADDRESS)
    app = DeepLabV3App(
        DeepLabV3PlusMobileNetQuantizable.from_pretrained().convert_to_quantized_torchscript(),
        num_classes=NUM_CLASSES,
    )
    app_output_image = app.predict(image, False)

    assert_most_close(
        np.asarray(app_output_image, dtype=np.float32) / 255,
        np.asarray(output_image, dtype=np.float32) / 255,
        diff_tol=0.005,
        rtol=0.02,
        atol=0.2,
    )


@skip_clone_repo_check
def test_aimet_export():
    model = DeepLabV3PlusMobileNetQuantizable.from_pretrained()
    name = model.__class__.__name__
    with tempfile.TemporaryDirectory() as tmpdir:
        output_zip = model.convert_to_onnx_and_aimet_encodings(
            tmpdir,
        )
        assert os.path.exists(output_zip)
        with zipfile.ZipFile(output_zip, "r") as zip:
            assert zip.namelist() == [
                f"{name}.aimet/",
                f"{name}.aimet/{name}.onnx",
                f"{name}.aimet/{name}.encodings",
            ]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_zip = model.convert_to_torchscript_and_aimet_encodings(
            tmpdir,
        )
        assert os.path.exists(output_zip)
        with zipfile.ZipFile(output_zip, "r") as zip:
            assert zip.namelist() == [
                f"{name}.aimet/",
                f"{name}.aimet/{name}.pt",
                f"{name}.aimet/{name}_torch.encodings",
            ]


@skip_clone_repo_check
def test_demo():
    demo_main(is_test=True)
