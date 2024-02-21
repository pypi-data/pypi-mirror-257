import pytest
import torch

from qai_hub_models.utils.base_model import BaseModel
from qai_hub_models.utils.internal.quantization_torch import (
    QuantizableMixin,
    module_is_quantized,
)


class ToyDenseNet(BaseModel, QuantizableMixin):
    def __init__(self):
        super(ToyDenseNet, self).__init__()
        self.fc = torch.nn.Linear(10, 5)

    def forward(self, x):
        x = self.fc(x)
        return x

    def get_input_spec(self):
        return {"x": ((2, 10), "float32")}

    def from_pretrained(self):
        pass


class ToyReluNet(torch.nn.Module):
    def forward(self, x):
        return torch.nn.functional.relu(x)


@pytest.mark.parametrize(
    "module_cls,detectable",
    [
        (ToyDenseNet, True),
        (ToyReluNet, False),
    ],
)
def test_module_is_quantized(module_cls, detectable):
    model = module_cls()

    model.eval()
    assert not module_is_quantized(model)

    engine = "qnnpack"
    torch.backends.quantized.engine = engine
    model.qconfig = torch.ao.quantization.get_default_qconfig(engine)

    torch.ao.quantization.prepare(model, inplace=True)
    torch.ao.quantization.convert(model, inplace=True)
    if detectable:
        assert module_is_quantized(model)
    else:
        assert not module_is_quantized(model)


def test_dummy_ptq():
    net = ToyDenseNet()
    with pytest.warns(UserWarning, match=r".*model will not be numerically accurate.*"):
        net.post_train_quantization()
    assert module_is_quantized(net)
