from qai_hub_models.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
    run_imagenet_classifier_trace_test,
)
from qai_hub_models.models.mobilenet_v2_tv.demo import main as demo_main
from qai_hub_models.models.mobilenet_v2_tv.model import MODEL_ID, MobileNetV2TV


def test_numerical():
    run_imagenet_classifier_test(
        MobileNetV2TV.from_pretrained(), MODEL_ID, probability_threshold=0.39
    )


def test_trace():
    run_imagenet_classifier_trace_test(MobileNetV2TV.from_pretrained())


def test_demo():
    # Verify demo does not crash
    demo_main(is_test=True)
