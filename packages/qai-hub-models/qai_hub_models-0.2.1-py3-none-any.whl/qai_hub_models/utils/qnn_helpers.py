from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import torch
from qai_hub.client import Job, Model, SourceModelType


def onnx_elem_type_to_str(elem_type: int) -> str:
    if elem_type == 1:
        return "float32"
    elif elem_type == 2:
        return "uint8"
    elif elem_type == 3:
        return "int8"
    elif elem_type == 6:
        return "int8"
    elif elem_type == 10:
        return "float16"
    raise ValueError("Unsupported elem_type.")


def load_encodings(output_path: Path, model_name: str) -> Dict:
    encodings_file = output_path / f"{model_name}.aimet" / f"{model_name}.encodings"
    with open(encodings_file) as f:
        encodings = json.load(f)
    return encodings["activation_encodings"]


def get_qnn_inputs(compile_job: Job, sample_inputs: Dict[str, List[torch.Tensor]]):
    compile_job.target_shapes
    return dict(zip(compile_job.target_shapes.keys(), sample_inputs.values()))


def is_qnn_hub_model(model: Model):
    return model.model_type in [
        SourceModelType.QNN_BIN,
        SourceModelType.QNN_LIB_AARCH64_ANDROID,
        SourceModelType.QNN_LIB_X86_64_LINUX,
    ]


def qnn_to_torch_outputs(
    outputs: List[torch.Tensor] | torch.Tensor,
) -> List[torch.Tensor] | torch.Tensor:
    """
    Converts QNN output to the same output if it came from PyTorch.

    If the input is a list, returns a list. If the input is a tensor, returns a tensor.
    """
    return_tensor = isinstance(outputs, torch.Tensor)
    if return_tensor:
        outputs = [outputs]  # type: ignore

    # qnn assets return transposed outputs when compared to PyTorch
    transposed_outputs = []
    for output in outputs:
        if len(output.shape) >= 4:
            transposed_outputs.append(output.moveaxis(-1, -3))
        else:
            transposed_outputs.append(output)

    return transposed_outputs[0] if return_tensor else transposed_outputs
