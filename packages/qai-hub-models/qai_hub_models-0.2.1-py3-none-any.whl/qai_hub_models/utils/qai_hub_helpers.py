from __future__ import annotations

import os
from typing import List

import qai_hub as hub
from qai_hub.client import APIException, UserError

from qai_hub_models.utils.asset_loaders import ASSET_CONFIG
from qai_hub_models.utils.base_model import TargetRuntime
from qai_hub_models.utils.config_loaders import QAIHMModelPerf
from qai_hub_models.utils.huggingface import fetch_huggingface_target_model
from qai_hub_models.utils.printing import print_profile_metrics


def can_access_qualcomm_ai_hub():
    try:
        hub.get_devices()
    except APIException:
        return False
    except UserError:
        return False
    return True


def export_without_hub_access(
    model_id: str,
    model_display_name: str,
    device_name: str,
    skip_profiling: bool,
    skip_inferencing: bool,
    skip_downloading: bool,
    skip_summary: bool,
    output_path: str,
    target_runtime: TargetRuntime,
    compile_options: str,
    profile_options: str,
    components: List[str] | None = None,
) -> List[str] | None:
    print(
        "Unable to find credentials for Qualcomm® AI Hub. Using results from a recently cached job on https://qaihub.qualcomm.com/."
    )
    print("")

    if compile_options or profile_options:
        raise NotImplementedError(
            "Compile and profile options are not supported without Qualcomm® AI Hub access."
        )

    if not skip_profiling and not skip_summary:
        print("")

        missing_perf = True
        # Components in perf.yaml don't yet have the same name as their code generated names.
        if not components:
            perf_yaml_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "models",
                model_id,
                "perf.yaml",
            )
            if os.path.exists(perf_yaml_path):
                parsed_perf = QAIHMModelPerf(perf_yaml_path, model_id).get_perf_details(
                    target_runtime, device_name
                )
                missing_perf = None in parsed_perf.values()

            if not missing_perf:
                print(
                    f"Pre-Generated Profiling Results for {model_display_name}\n"
                    f"{'-' * 50}"
                )
                for model_name, perf in parsed_perf.items():
                    assert perf is not None  # for mypy
                    print(f"\n{model_name}\n" f"{'-' * 50}")
                    print_profile_metrics(perf)

        if missing_perf:
            print(
                f"Cached results unavaliable for Device({device_name}) with runtime {target_runtime.name}.\n"
                "Please sign up to Qualcomm® AI Hub to get access get performance metrics for this configuration."
            )

        print("")

    if not skip_inferencing and not skip_summary:
        print(
            "\nSkipping inference. Unable to schedule an inference job without credentials for Qualcomm® AI Hub.\n"
        )

    paths = []
    if not skip_downloading:
        print("")
        print(
            f"Downloading pre-exported model(s) from Hugging Face ({ASSET_CONFIG.get_hugging_face_url(model_display_name)})."
        )
        try:
            paths = fetch_huggingface_target_model(
                model_display_name, output_path, target_runtime
            )
            print(f"Saved exported model(s) at: {paths}")
        except Exception as e:
            print(f"Download failure: {e}")
        print("")

    print(
        "\nTo run export, profile, or inference jobs for these models on-demand on hosted Qualcomm powered devices, please sign up for Qualcomm® AI Hub at https://qaihub.qualcomm.com/."
    )

    return paths
