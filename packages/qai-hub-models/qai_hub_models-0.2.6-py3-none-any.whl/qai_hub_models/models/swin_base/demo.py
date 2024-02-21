from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.swin_base.model import SwinBase


def main(is_test: bool = False):
    imagenet_demo(SwinBase, is_test)


if __name__ == "__main__":
    main()
