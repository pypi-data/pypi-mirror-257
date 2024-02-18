from qai_hub_models.models._shared.super_resolution.demo import super_resolution_demo
from qai_hub_models.models.xlsr_quantized.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    XLSRQuantizable,
)
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset

IMAGE_ADDRESS = CachedWebModelAsset.from_asset_store(
    MODEL_ID, MODEL_ASSET_VERSION, "xlsr_quantized_demo.jpg"
)


def main(is_test: bool = False):
    super_resolution_demo(XLSRQuantizable, IMAGE_ADDRESS, is_test)


if __name__ == "__main__":
    main()
