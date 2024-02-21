from qai_hub_models.models._shared.imagenet_classifier.test_utils import (
    TEST_IMAGENET_IMAGE,
)
from qai_hub_models.models.mobiledet import App, Model
from qai_hub_models.utils.asset_loaders import load_image


def main():
    image = load_image(TEST_IMAGENET_IMAGE)
    app = App(Model.from_pretrained())
    app.predict(image)


if __name__ == "__main__":
    main()
