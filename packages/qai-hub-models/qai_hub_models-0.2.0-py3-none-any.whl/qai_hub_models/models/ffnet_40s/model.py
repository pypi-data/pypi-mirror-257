from __future__ import annotations

from qai_hub_models.models._shared.ffnet.model import FFNet

MODEL_ID = __name__.split(".")[-2]


class FFNet40S(FFNet):
    @classmethod
    def from_pretrained(cls) -> FFNet40S:
        return FFNet.from_pretrained.__func__(cls, "segmentation_ffnet40S_dBBB_mobile")
