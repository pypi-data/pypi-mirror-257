from qai_hub_models.models._shared.imagenet_classifier.demo import imagenet_demo
from qai_hub_models.models.inception_v3_quantized.model import InceptionNetV3Quantizable


def main(is_test: bool = False):
    imagenet_demo(InceptionNetV3Quantizable, is_test)


if __name__ == "__main__":
    main()
