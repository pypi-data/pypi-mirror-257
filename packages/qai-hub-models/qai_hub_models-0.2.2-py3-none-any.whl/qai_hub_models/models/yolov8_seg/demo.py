from __future__ import annotations

import os
from typing import Callable, Tuple

import torch

from qai_hub_models.models.yolov8_seg.app import YoloV8SegmentationApp
from qai_hub_models.models.yolov8_seg.model import (
    DEFAULT_WEIGHTS,
    MODEL_ASSET_VERSION,
    MODEL_ID,
    YoloV8Segmentor,
)
from qai_hub_models.utils.args import (
    demo_model_from_cli_args,
    get_model_cli_parser,
    get_on_device_demo_parser,
    validate_on_device_demo_args,
)
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, load_image
from qai_hub_models.utils.base_model import TargetRuntime

WEIGHTS_HELP_MSG = f"YoloV8-Segment checkpoint name. Valid checkpoints can be found in qai_hub_models/{MODEL_ID}/model.py"

IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, "test_images/bus.jpg"
)
OUTPUT_IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, "test_images/out_bus_with_mask.png"
)


def yolov8_seg_demo(
    model_type: Callable[
        ...,
        Callable[
            [torch.Tensor],
            Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor],
        ],
    ],
    default_weights: str,
    weights_help_msg: str,
    default_image: str,
    stride_multiple: int | None = None,
    is_test: bool = False,
):
    # Demo parameters
    parser = get_model_cli_parser(model_type)
    parser = get_on_device_demo_parser(
        parser, available_target_runtimes=[TargetRuntime.TFLITE]
    )
    image_help = "image file path or URL."
    if stride_multiple:
        image_help = f"{image_help} Image spatial dimensions (x and y) must be multiples of {stride_multiple}."

    parser.add_argument(
        "--image",
        type=str,
        help="Test image file path or URL",
    )
    parser.add_argument(
        "--score_threshold",
        type=float,
        default=0.45,
        help="Score threshold for NonMaximumSuppression",
    )
    parser.add_argument(
        "--iou_threshold",
        type=float,
        default=0.7,
        help="Intersection over Union (IoU) threshold for NonMaximumSuppression",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="if specified, will output the results to this folder instead of a pop-up window",
    )

    args = parser.parse_args([] if is_test else None)
    validate_on_device_demo_args(args, model_type.get_model_id())

    if args.image is None:
        image_path = default_image.fetch()
    else:
        image_path = args.image

    # Load image & model
    model = demo_model_from_cli_args(model_type, args, check_trace=False)
    app = YoloV8SegmentationApp(model, args.score_threshold, args.iou_threshold)

    print("Model Loaded")

    image = load_image(image_path)
    image_annotated = app.predict_segmentation_from_image(image)[0]

    if args.output_dir:
        output_path = os.path.join(args.output_dir, os.path.basename(image_path))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image_annotated.save(output_path)
    elif not is_test:
        image_annotated.show()


def main(is_test: bool = False):
    yolov8_seg_demo(
        YoloV8Segmentor,
        DEFAULT_WEIGHTS,
        WEIGHTS_HELP_MSG,
        IMAGE_ADDRESS,
        is_test=is_test,
    )


if __name__ == "__main__":
    main()
