from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import qai_hub as hub
from qai_hub.client import SourceModelType

from qai_hub_models.utils.base_model import TargetRuntime
from qai_hub_models.utils.compare import generate_comparison_metrics
from qai_hub_models.utils.config_loaders import QAIHMModelPerf
from qai_hub_models.utils.qnn_helpers import is_qnn_hub_model


def print_inference_metrics(
    inference_job: hub.InferenceJob,
    inference_result: Dict[str, List[np.ndarray]],
    torch_out: List[np.ndarray],
    outputs_to_skip: Optional[List[int]] = None,
) -> None:
    inference_data = [
        np.concatenate(outputs, axis=0) for outputs in inference_result.values()
    ]
    metrics = generate_comparison_metrics(torch_out, inference_data)
    last_line = f"More details at ({inference_job.url})."
    print(
        f"\nInference Job Summary for {inference_job.name.title()}.\n"
        f"{last_line}\n"
        f"{'-' * len(last_line)}\n"
        "\nMetrics comparing on-device inference vs. local cpu\n"
    )
    outputs_to_skip = outputs_to_skip or []
    i = 0
    while i in metrics or i in outputs_to_skip:
        if i in outputs_to_skip or np.prod(np.array(metrics[i].shape)) < 5:
            print(f"PSNR check skipped for output #{i}.\n")
            i += 1
            continue
        print(f"Output #{i} has shape {metrics[i].shape}.")
        print(
            f"Peak Signal-to-Noise Ratio (PSNR) on output #{i}: "
            f"{metrics[i].psnr:.4g} dB\n"
        )
        i += 1


def print_profile_metrics_from_job(
    profile_job: hub.ProfileJob,
    profile_data: Dict[str, Any],
):
    compute_unit_counts = Counter(
        [op.get("compute_unit", "UNK") for op in profile_data["execution_detail"]]
    )
    execution_summary = profile_data["execution_summary"]
    inference_time_ms = execution_summary["estimated_inference_time"] / 1000
    peak_memory_bytes = execution_summary["inference_memory_peak_range"]
    last_line = f"More details at ({profile_job.url})."
    print(
        f"\nProfile Job Summary for {profile_job.name.title()}.\n{last_line}\n{'-' * len(last_line)}\n"
    )

    if profile_job.model.model_type == SourceModelType.TFLITE:
        runtime = TargetRuntime.TFLITE
    elif is_qnn_hub_model(profile_job.model):
        runtime = TargetRuntime.QNN
    else:
        raise NotImplementedError()

    print_profile_metrics(
        QAIHMModelPerf.ModelRuntimePerformanceDetails(
            profile_job.model.name,
            profile_job.device.name,
            profile_job.device.os,
            runtime,
            inference_time_ms,
            peak_memory_bytes,
            compute_unit_counts,
        )
    )


def print_profile_metrics(
    details: QAIHMModelPerf.ModelRuntimePerformanceDetails,
):
    print(f"Device: {details.device_name} ({details.device_os})")
    print(f"Runtime: {details.runtime.name}")
    if details.inference_time_ms < 0.1:
        print("Estimated Inference Time: less than 0.1ms")
    else:
        print(f"Estimated Inference Time: {details.inference_time_ms:.1f}ms")
    print(
        "Estimated Peak Memory Usage: "
        f"{round(details.peak_memory_bytes[0] / 1e6)}-{round(details.peak_memory_bytes[1] / 1e6)} MB"
    )
    print("Compute Units:", end="")
    for unit, num_ops in details.compute_unit_counts.items():
        print(f" {unit} ({num_ops} ops)", end="")
        print("")  # newline
    if len(details.compute_unit_counts) > 1:
        print(f"Total Number of Ops: {sum(details.compute_unit_counts.values())}")


def print_on_target_demo_cmd(
    compile_job: hub.CompileJob, model_folder: Path, device: str
) -> None:
    """
    Outputs a command that will run a model's demo script via inference job.
    """
    assert compile_job.wait().success
    print("To demo this compiled model using on-device inference of real data run:\n")
    target_model = compile_job.get_target_model()
    assert target_model is not None
    print(
        f"python {model_folder / 'demo.py'} "
        "--on-device "
        f"--hub-model-id {target_model.model_id} "
        f'--device "{device}"\n'
    )
