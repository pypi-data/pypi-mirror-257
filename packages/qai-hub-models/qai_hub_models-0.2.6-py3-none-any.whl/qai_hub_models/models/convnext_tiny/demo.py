from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.convnext_tiny.model import ConvNextTiny


def main(is_test: bool = False):
    imagenet_demo(ConvNextTiny, is_test)


if __name__ == "__main__":
    main()
