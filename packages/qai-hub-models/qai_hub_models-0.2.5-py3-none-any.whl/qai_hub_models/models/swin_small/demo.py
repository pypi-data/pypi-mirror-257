from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.swin_small.model import SwinSmall


def main(is_test: bool = False):
    imagenet_demo(SwinSmall, is_test)


if __name__ == "__main__":
    main()
