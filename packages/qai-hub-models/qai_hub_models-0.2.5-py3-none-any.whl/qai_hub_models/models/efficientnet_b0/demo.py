from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.efficientnet_b0.model import EfficientNetB0


def main(is_test: bool = False):
    imagenet_demo(EfficientNetB0, is_test)


if __name__ == "__main__":
    main()
