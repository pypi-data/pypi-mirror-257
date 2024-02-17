import os

from qai_hub_models.models.ddrnet23_slim.app import DDRNetApp
from qai_hub_models.models.ddrnet23_slim.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    DDRNet,
)
from qai_hub_models.utils.args import (
    demo_model_from_cli_args,
    get_model_cli_parser,
    get_on_device_demo_parser,
    validate_on_device_demo_args,
)
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, load_image

INPUT_IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, "test_input_image.png"
)


# Run DDRNet end-to-end on a sample image.
# The demo will display a image with the predicted segmentation map overlaid.
def main(is_test: bool = False):
    # Demo parameters
    parser = get_model_cli_parser(DDRNet)
    parser = get_on_device_demo_parser(parser)
    parser.add_argument(
        "--image",
        type=str,
        default=INPUT_IMAGE_ADDRESS,
        help="image file path or URL",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        default=None,
        help="If specified, saves output image to this directory instead of showing.",
    )
    args = parser.parse_args([] if is_test else None)
    model = demo_model_from_cli_args(DDRNet, args)
    validate_on_device_demo_args(args, DDRNet.get_model_id())

    # Load image & model
    image = load_image(args.image)
    print("Model Loaded")

    app = DDRNetApp(model)
    output = app.segment_image(image)[0]
    if not is_test:
        if args.output_path:
            filename = os.path.join(args.output_path, "ddrnet_demo_output.png")
            print(f"Output written to {filename}")
            output.save(filename)
        else:
            output.show()


if __name__ == "__main__":
    main()
