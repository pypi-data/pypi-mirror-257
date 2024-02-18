from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.shufflenet_v2.model import ShufflenetV2


def main(is_test: bool = False):
    imagenet_demo(ShufflenetV2, is_test)


if __name__ == "__main__":
    main()
