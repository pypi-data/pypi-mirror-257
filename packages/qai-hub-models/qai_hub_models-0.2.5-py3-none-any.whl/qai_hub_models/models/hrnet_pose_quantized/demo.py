from qai_hub_models.models.hrnet_pose.app import HRNetPoseApp
from qai_hub_models.models.hrnet_pose_quantized.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    HRNetPoseQuantizable,
)
from qai_hub_models.utils.args import get_model_cli_parser, model_from_cli_args
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, load_image
from qai_hub_models.utils.display import display_image

IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, "hrnet_pose_demo.png"
)


# The demo will display a image with the predicted keypoints.
def main(is_test: bool = False):
    # Demo parameters
    parser = get_model_cli_parser(HRNetPoseQuantizable)
    parser.add_argument(
        "--image",
        type=str,
        default=IMAGE_ADDRESS,
        help="image file path or URL",
    )

    args = parser.parse_args([] if is_test else None)

    # Load image & model
    model = model_from_cli_args(HRNetPoseQuantizable, args)
    image = load_image(args.image)
    print("Model Loaded")

    app = HRNetPoseApp(model)
    keypoints = app.predict_pose_keypoints(image)[0]
    if not is_test:
        display_image(keypoints)


if __name__ == "__main__":
    main()
