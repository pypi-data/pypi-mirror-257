from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.regnet_quantized.model import RegNetQuantizable


def main(is_test: bool = False):
    imagenet_demo(RegNetQuantizable, is_test)


if __name__ == "__main__":
    main()
