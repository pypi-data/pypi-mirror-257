from __future__ import annotations

from qai_hub_models.models._shared.ffnet.model import FFNet

MODEL_ID = __name__.split(".")[-2]


class FFNet54S(FFNet):
    @classmethod
    def from_pretrained(cls) -> FFNet54S:
        return FFNet.from_pretrained.__func__(cls, "segmentation_ffnet54S_dBBB_mobile")
