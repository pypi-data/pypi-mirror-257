from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.mnasnet05.model import MNASNet05


def main(is_test: bool = False):
    imagenet_demo(MNASNet05, is_test)


if __name__ == "__main__":
    main()
