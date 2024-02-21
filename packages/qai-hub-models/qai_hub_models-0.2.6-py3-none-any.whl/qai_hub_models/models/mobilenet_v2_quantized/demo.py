from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.mobilenet_v2_quantized.model import MobileNetV2Quantizable


def main(is_test: bool = False):
    imagenet_demo(MobileNetV2Quantizable, is_test)


if __name__ == "__main__":
    main()
