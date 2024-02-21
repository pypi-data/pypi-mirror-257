from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.googlenet_quantized.model import GoogLeNetQuantizable


def main(is_test: bool = False):
    imagenet_demo(GoogLeNetQuantizable, is_test)


if __name__ == "__main__":
    main()
