from qai_hub_models.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
    run_imagenet_classifier_trace_test,
)
from qai_hub_models.models.googlenet.demo import main as demo_main
from qai_hub_models.models.googlenet.model import MODEL_ID, GoogLeNet


def test_task():
    run_imagenet_classifier_test(GoogLeNet.from_pretrained(), MODEL_ID)


def test_trace():
    run_imagenet_classifier_trace_test(GoogLeNet.from_pretrained())


def test_demo():
    # Verify demo does not crash
    demo_main(is_test=True)
