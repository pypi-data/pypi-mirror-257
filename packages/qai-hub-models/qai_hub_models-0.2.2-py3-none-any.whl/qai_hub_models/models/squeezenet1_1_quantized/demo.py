from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.squeezenet1_1_quantized.model import SqueezeNetQuantizable


def main(is_test: bool = False):
    imagenet_demo(SqueezeNetQuantizable, is_test)


if __name__ == "__main__":
    main()
