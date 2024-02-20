from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.resnext101.model import ResNeXt101


def main(is_test: bool = False):
    imagenet_demo(ResNeXt101, is_test)


if __name__ == "__main__":
    main()
