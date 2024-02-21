from qai_hub_models.models._shared.cityscapes_segmentation.demo import (
    cityscapes_segmentation_demo,
)
from qai_hub_models.models.ffnet_78s_quantized.model import (
    MODEL_ID,
    FFNet78SQuantizable,
)


def main(is_test: bool = False):
    cityscapes_segmentation_demo(
        FFNet78SQuantizable, MODEL_ID, transpose_io=True, is_test=is_test
    )


if __name__ == "__main__":
    main()
