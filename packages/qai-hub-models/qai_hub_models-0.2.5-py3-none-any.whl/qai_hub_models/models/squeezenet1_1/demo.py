from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.squeezenet1_1.model import SqueezeNet


def main(is_test: bool = False):
    imagenet_demo(SqueezeNet, is_test)


if __name__ == "__main__":
    main()
