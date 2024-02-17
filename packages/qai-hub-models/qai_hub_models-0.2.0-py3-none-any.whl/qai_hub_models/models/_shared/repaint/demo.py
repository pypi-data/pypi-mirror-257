from __future__ import annotations

import os
from typing import Type

from qai_hub_models.models._shared.repaint.app import RepaintMaskApp
from qai_hub_models.utils.args import (
    demo_model_from_cli_args,
    get_model_cli_parser,
    get_on_device_demo_parser,
    validate_on_device_demo_args,
)
from qai_hub_models.utils.asset_loaders import CachedWebAsset, load_image
from qai_hub_models.utils.base_model import BaseModel, TargetRuntime


# Run repaint app end-to-end on a sample image.
# The demo will display the predicted image in a window.
def repaint_demo(
    model_type: Type[BaseModel],
    default_image: str | CachedWebAsset,
    default_mask: str | CachedWebAsset,
    is_test: bool = False,
):
    # Demo parameters
    parser = get_model_cli_parser(model_type)
    parser = get_on_device_demo_parser(
        parser, available_target_runtimes=[TargetRuntime.TFLITE]
    )
    parser.add_argument(
        "--image",
        type=str,
        default=default_image,
        help="test image file path or URL",
    )
    parser.add_argument(
        "--mask",
        type=str,
        default=default_mask,
        help="test mask file path or URL",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="If specified, will output the results to this folder instead of a pop-up window",
    )
    args = parser.parse_args([] if is_test else None)
    validate_on_device_demo_args(args, model_type.get_model_id())

    # Load image & model
    model = demo_model_from_cli_args(model_type, args)
    image = load_image(args.image)
    mask = load_image(args.mask)
    print("Model Loaded")

    # Run app
    app = RepaintMaskApp(model)
    if not is_test and not args.output_dir:
        image.show(title="Model Input")
    out = app.paint_mask_on_image(image, mask)[0]

    if args.output_dir:
        output_path = os.path.join(args.output_dir, "output.png")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        out.save(output_path)
    elif not is_test:
        out.show("Repainted (Model Output)")
