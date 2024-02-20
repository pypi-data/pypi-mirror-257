from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.inception_v3.model import InceptionNetV3


def main(is_test: bool = False):
    imagenet_demo(InceptionNetV3, is_test)


if __name__ == "__main__":
    main()
