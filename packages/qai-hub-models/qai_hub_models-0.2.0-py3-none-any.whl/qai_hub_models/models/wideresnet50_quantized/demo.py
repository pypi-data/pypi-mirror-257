from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.wideresnet50_quantized.model import WideResNet50Quantizable


def main(is_test: bool = False):
    imagenet_demo(WideResNet50Quantizable, is_test)


if __name__ == "__main__":
    main()
