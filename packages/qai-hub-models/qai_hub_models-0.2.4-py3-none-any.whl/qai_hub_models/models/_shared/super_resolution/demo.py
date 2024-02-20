from __future__ import annotations

from typing import Type

import qai_hub as hub

from qai_hub_models.models._shared.super_resolution.app import SuperResolutionApp
from qai_hub_models.utils.args import get_model_cli_parser, model_from_cli_args
from qai_hub_models.utils.asset_loaders import CachedWebAsset, load_image
from qai_hub_models.utils.base_model import BaseModel
from qai_hub_models.utils.display import display_image
from qai_hub_models.utils.inference import HubModel


# Run Super Resolution end-to-end on a sample image.
# The demo will display both the input image and the higher resolution output.
def super_resolution_demo(
    model_cls: Type[BaseModel],
    default_image: str | CachedWebAsset,
    is_test: bool = False,
):
    # Demo parameters
    parser = get_model_cli_parser(model_cls)
    parser.add_argument(
        "--image",
        type=str,
        default=default_image,
        help="image file path or URL.",
    )
    parser.add_argument(
        "--on-device",
        action="store_true",
        help="If set, will evalute model using hub inference job instead of torch.",
    )
    parser.add_argument(
        "--hub-model-id",
        type=str,
        default=None,
        help="If running on device inference, uses this model id.",
    )
    parser.add_argument(
        "--hub-compile-job-id",
        type=str,
        default=None,
        help="If running on device inference, uses this compile job to get the model",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="Samsung Galaxy S23",
        help="If running on hub inference job, use this device.",
    )

    args = parser.parse_args([] if is_test else None)

    # Load image & model
    model = model_from_cli_args(model_cls, args)
    if args.on_device:
        input_names = list(model.get_input_spec().keys())
        model_id = args.hub_model_id
        if model_id is None and args.hub_compile_job_id is not None:
            model_id = hub.get_job(args.hub_compile_job_id).get_target_model().model_id
        hub_model = HubModel(input_names, args.device, model_id, model)
        app = SuperResolutionApp(hub_model)
    else:
        app = SuperResolutionApp(model)
    print("Model Loaded")
    image = load_image(args.image)
    pred_images = app.upscale_image(image)
    if not is_test:
        display_image(image)
        display_image(pred_images[0])
