from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.resnet101.model import ResNet101


def main(is_test: bool = False):
    imagenet_demo(ResNet101, is_test)


if __name__ == "__main__":
    main()
