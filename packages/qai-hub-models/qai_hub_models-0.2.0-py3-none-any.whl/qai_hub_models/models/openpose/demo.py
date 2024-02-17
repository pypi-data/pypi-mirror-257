import argparse

from qai_hub_models.models.openpose.app import OpenPoseApp
from qai_hub_models.models.openpose.model import MODEL_ASSET_VERSION, MODEL_ID, OpenPose
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset, load_image

IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, "openpose_demo.png"
)


# Run OpenPose end-to-end on a sample image.
# The demo will display the input image with circles drawn over the estimated joint positions.
def main(is_test: bool = False):
    # Demo parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image",
        type=str,
        default=IMAGE_ADDRESS,
        help="image file path or URL.",
    )

    args = parser.parse_args([] if is_test else None)

    # Load image & model
    app = OpenPoseApp(OpenPose.from_pretrained())
    image = load_image(args.image)
    pred_images = app.estimate_pose(image)
    if not is_test:
        pred_images.show()


if __name__ == "__main__":
    main()
