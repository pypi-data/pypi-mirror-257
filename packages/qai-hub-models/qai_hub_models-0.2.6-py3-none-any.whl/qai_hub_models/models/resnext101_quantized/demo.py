from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.resnext101_quantized.model import ResNeXt101Quantizable


def main(is_test: bool = False):
    imagenet_demo(ResNeXt101Quantizable, is_test)


if __name__ == "__main__":
    main()
