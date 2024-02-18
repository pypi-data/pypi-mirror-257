from qai_hub_models.models.litehrnet.app import LiteHRNetApp
from qai_hub_models.models.litehrnet.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    LiteHRNet,
)
from qai_hub_models.utils.args import get_model_cli_parser, model_from_cli_args
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, load_image

IA_HELP_MSG = "More inferencer architectures for litehrnet can be found at https://github.com/open-mmlab/mmpose/tree/main/configs/body_2d_keypoint/topdown_heatmap/coco"
IMAGE_LOCAL_PATH = "litehrnet_demo.png"
IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, IMAGE_LOCAL_PATH
)


# Run LiteHRNet end-to-end on a sample image.
# The demo will display a image with the predicted keypoints.
def main(is_test: bool = False):
    # Demo parameters
    parser = get_model_cli_parser(LiteHRNet)
    parser.add_argument(
        "--image",
        type=str,
        default=IMAGE_ADDRESS,
        help="image file path or URL",
    )

    args = parser.parse_args([] if is_test else None)

    # Load image & model
    model = model_from_cli_args(LiteHRNet, args)
    image = load_image(args.image)
    print("Model Loaded")

    app = LiteHRNetApp(model, model.inferencer)
    keypoints = app.predict_pose_keypoints(image)[0]
    if not is_test:
        keypoints.show()


if __name__ == "__main__":
    main()
