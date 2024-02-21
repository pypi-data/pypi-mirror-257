from __future__ import annotations

import warnings
from typing import Iterator, Tuple

import torch
from torch.utils.data import DataLoader
from tqdm.autonotebook import tqdm

from qai_hub_models.utils.base_model import BaseModel

# To get the model id for a quantized model, append this to the MODEL_ID of the unquantized version
QUANTIZED_MODEL_ID_SUFFIX = "_quantized"


def module_is_quantized(model: torch.nn.Module):
    """
    This only works if torch.ao.quantization.convert makes a change to the
    models. Currently it's models with Linear or Conv. Models with only relu
    activation aren't changed by torch.ao.quantization.convert so cannot be
    detected.
    """
    for module in model.modules():
        # List of quantized layer types can be expanded as needed
        if isinstance(module, (torch.nn.quantized.Conv2d, torch.nn.quantized.Linear)):
            return True
    return False


class QuantizableMixin:
    """
    This mixin provides quantization support with torch.ao.quantization, using
    qnnpack by default.

    Basics of `torch.ao.quantization`:

    - An fp32 model can only be quantized (`torch.ao.quantization.convert`)
      exactly once and it's irreversible (a one way trip).

    - Model quantized by torch.ao.quantization is a distinct torch.nn.Module
      and have different state_dict keys than the original fp32 model.

    - There's no easy way to define the resulting torch.nn.Module produced by
      `torch.ao.quantization`. Therefore, the best practice is to always run
      this `torch.ao.quantization.convert` on fp32 to obtain int8
      torch.nn.Module.

    Given the above, the mixin advocates one of the following quantization user
    journeys:

    1. Grab and go without any data. The user may call
    `ModelNameQuantizable.from_pretrained("<some_int8_weight_name>")` to get
    the quantized weights for deployment (export w/ Hub etc). The weights are
    produced and maintained by Qualcomm AI Hub Models team with evaluation
    on standard benchmarks. The resulting `ModelNameQuantizable` may not be
    further quantized and is ready to be exported.

    Under the hood we do the followings:

    a. Initialize `ModelNameQuantizable` with fp32 weights
    b. Run dummy `post_train_quantization` on random data to produce int8
       model def.
    c. Load the checkpoint.

    2. DIY quantization and bring your own data. The user may bring their own
    data (for calibration and evaluation) and create their own model:

    a. Initialize `ModelNameQuantizable` with fp32 weights
    b. Run `post_train_quantization` on user data to produce int8
       model def.

    Observe that in both user stories `post_train_quantization` is called.
    Prior to this call, exporting `ModelNameQuantizable` is ill-defined. We'll
    print relevant warning messages about this.


    Implementation note: Do not subclass `torch.nn.Module` because that would
    invoke its __init__ method which clears out the members.
    """

    def prepare_ptq(self) -> None:
        """
        Prepare the model for post-training quantization. This installs "observers"
        into the model that will record min/max of any samples that pass through it.
        """
        engine = "qnnpack"
        torch.backends.quantized.engine = engine  # type: ignore
        self.qconfig = torch.ao.quantization.get_default_qconfig(engine)

        torch.ao.quantization.prepare(self, inplace=True)

    def make_dummy_data_loader(self) -> torch.utils.data.DataLoader:
        """
        Returns a dummy data loader to run post_train_quantization without
        any data.
        """
        warnings.warn(
            "Using dummy data to quantize model. The resulting "
            "model will not be numerically accurate.",
            UserWarning,
        )
        if not isinstance(self, BaseModel):
            raise ValueError(
                "Cannot generate random data without input "
                "spec. Please provide data to run "
                "post_train_quantization"
            )
        tensors = [
            torch.cat([torch.from_numpy(tensor) for tensor in tensor_list], dim=0)
            for tensor_list in self.sample_inputs().values()
        ]

        tensor_dataset = torch.utils.data.TensorDataset(*tensors)
        return DataLoader(tensor_dataset, batch_size=1)

    def post_train_quantization(
        self, data_loader: Iterator[Tuple[torch.Tensor, ...]] | None = None
    ) -> None:
        """
        Perform post-train quantization calibration given a tensor of
        quantization samples
        Parameters:
            data_loader: An iterator returning mini-batches of input data x
            (but not labels) where x is one or more torch.Tensor. We use ALL
            data from the iterator to perform PTQ calibration. If data_loader
            is None, we make a random sample and perform PTQ.
            Note: torch.utils.data.DataLoader satisfies the iterator interface
            here. Huggingface dataset can be easily adapted via
            >> from datasets import load_dataset
            >> dataset = load_dataset('some_dataset')
            >> data_loader = torch.utils.data.DataLoader(
            >>    dataset['train'], batch_size=32)
        """
        if not isinstance(self, torch.nn.Module):
            raise ValueError("Class is not a torch module")

        if module_is_quantized(self):  # type: ignore
            raise ValueError("Cannot quantize an already quantized model")

        if data_loader is None:
            if not isinstance(self, BaseModel):
                raise ValueError(
                    "Cannot generate random data without input "
                    "spec. Please provide data to run "
                    "post_train_quantization"
                )
            data_loader = self.make_dummy_data_loader()

        # Install observers
        self.prepare_ptq()

        # PTQ calibration using samples from data_loader
        with torch.inference_mode():
            for tensors in tqdm(data_loader):
                if isinstance(tensors, torch.Tensor):
                    tensors = (tensors,)
                _ = self(*tensors)

        # Finalize quantization
        torch.ao.quantization.convert(self, inplace=True)
