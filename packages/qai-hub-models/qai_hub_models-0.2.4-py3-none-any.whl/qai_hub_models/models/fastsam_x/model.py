from __future__ import annotations

from qai_hub_models.models._shared.fastsam.model import Fast_SAM

MODEL_ID = __name__.split(".")[-2]
DEFAULT_WEIGHTS = "FastSAM-x.pt"
MODEL_ASSET_VERSION = 1


class FastSAM_X(Fast_SAM):
    """Exportable FastSAM model, end-to-end."""

    @classmethod
    def from_pretrained(cls, ckpt_name: str = DEFAULT_WEIGHTS):
        return Fast_SAM.from_pretrained(ckpt_name)
