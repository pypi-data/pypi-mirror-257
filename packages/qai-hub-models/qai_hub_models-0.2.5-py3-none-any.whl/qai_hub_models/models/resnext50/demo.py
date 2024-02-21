from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.resnext50.model import ResNeXt50


def main(is_test: bool = False):
    imagenet_demo(ResNeXt50, is_test)


if __name__ == "__main__":
    main()
