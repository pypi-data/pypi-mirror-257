from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.resnet50.model import ResNet50


def main(is_test: bool = False):
    imagenet_demo(ResNet50, is_test)


if __name__ == "__main__":
    main()
