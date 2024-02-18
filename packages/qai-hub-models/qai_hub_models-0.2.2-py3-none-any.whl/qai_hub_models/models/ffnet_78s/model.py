from __future__ import annotations

from qai_hub_models.models._shared.ffnet.model import FFNet

MODEL_ID = __name__.split(".")[-2]


class FFNet78S(FFNet):
    @classmethod
    def from_pretrained(cls) -> FFNet78S:
        return FFNet.from_pretrained.__func__(cls, "segmentation_ffnet78S_dBBB_mobile")
