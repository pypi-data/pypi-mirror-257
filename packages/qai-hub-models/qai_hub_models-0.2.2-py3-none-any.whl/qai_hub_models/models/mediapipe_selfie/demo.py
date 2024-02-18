from __future__ import annotations

from typing import Callable

import torch
from PIL.Image import fromarray

from qai_hub_models.models.mediapipe_selfie.app import SelfieSegmentationApp
from qai_hub_models.models.mediapipe_selfie.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    SelfieSegmentation,
)
from qai_hub_models.utils.args import get_model_cli_parser, model_from_cli_args
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, load_image

IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, "selfie.jpg"
)


# Run selfie segmentation app end-to-end on a sample image.
# The demo will display the predicted mask in a window.
def mediapipe_selfie_demo(
    model_cls: Callable[..., Callable[[torch.Tensor, torch.Tensor], torch.Tensor]],
    default_image: str | CachedWebModelAsset,
    is_test: bool = False,
):
    # Demo parameters
    parser = get_model_cli_parser(model_cls)
    parser.add_argument(
        "--image",
        type=str,
        default=default_image,
        help="test image file path or URL",
    )
    args = parser.parse_args([] if is_test else None)

    # Load image & model
    model = model_from_cli_args(model_cls, args)
    image = load_image(args.image)
    print("Model Loaded")

    # Run app
    app = SelfieSegmentationApp(model)
    if not is_test:
        image.show(title="Model Input")
    mask = app.predict(image) * 255.0
    mask = fromarray(mask).convert("L")
    if not is_test:
        mask.show(title="Mask (Model Output)")


def main(is_test: bool = False):
    mediapipe_selfie_demo(
        SelfieSegmentation,
        IMAGE_ADDRESS,
        is_test,
    )


if __name__ == "__main__":
    main()
