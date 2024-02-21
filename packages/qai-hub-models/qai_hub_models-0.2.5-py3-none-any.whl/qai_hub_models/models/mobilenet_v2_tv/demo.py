from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.mobilenet_v2_tv.model import MobileNetV2TV


def main(is_test: bool = False):
    imagenet_demo(MobileNetV2TV, is_test)


if __name__ == "__main__":
    main()
