import os

from qai_hub_models.models.sinet.app import SINetApp
from qai_hub_models.models.sinet.model import MODEL_ASSET_VERSION, MODEL_ID, SINet
from qai_hub_models.utils.args import (
    demo_model_from_cli_args,
    get_model_cli_parser,
    get_on_device_demo_parser,
    validate_on_device_demo_args,
)
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, load_image

INPUT_IMAGE_LOCAL_PATH = "sinet_demo.png"
INPUT_IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, INPUT_IMAGE_LOCAL_PATH
)


def main(is_test: bool = False):
    # Demo parameters
    parser = get_model_cli_parser(SINet)
    parser = get_on_device_demo_parser(parser)
    parser.add_argument(
        "--image",
        type=str,
        default=INPUT_IMAGE_ADDRESS,
        help="image file path or URL.",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        default=None,
        help="If specified, saves output image to this directory instead of showing.",
    )
    args = parser.parse_args([] if is_test else None)
    model = demo_model_from_cli_args(SINet, args)
    validate_on_device_demo_args(args, SINet.get_model_id())

    # load image and model
    image = load_image(args.image)
    input_image = image.convert("RGB")
    app = SINetApp(model)
    output = app.predict(input_image, False, False)
    if not is_test:
        if args.output_path:
            filename = os.path.join(args.output_path, "sinet_demo_output.png")
            print(f"Output written to {filename}")
            output.save(filename)
        else:
            output.show()


if __name__ == "__main__":
    main()
