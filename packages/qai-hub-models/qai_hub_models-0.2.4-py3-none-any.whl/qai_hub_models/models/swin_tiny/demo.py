from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.swin_tiny.model import SwinTiny


def main(is_test: bool = False):
    imagenet_demo(SwinTiny, is_test)


if __name__ == "__main__":
    main()
