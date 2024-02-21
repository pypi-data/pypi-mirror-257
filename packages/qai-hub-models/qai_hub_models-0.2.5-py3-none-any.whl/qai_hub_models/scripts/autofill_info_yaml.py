import argparse
import importlib
import os
import subprocess
import tempfile
import traceback

import qai_hub as hub
import torch
from ruamel.yaml import YAML

from qai_hub_models.utils.input_spec import make_torch_inputs
from qai_hub_models.utils.measurement import (
    get_checkpoint_file_size,
    get_tflite_unique_parameters,
)
from qai_hub_models.utils.path_helpers import get_all_models, get_qaihm_models_root
from qai_hub_models.utils.quantization_aimet import AIMETQuantizableMixin


def trace_model(model, input_spec):
    # Trace the model
    if issubclass(model.__class__, AIMETQuantizableMixin):
        # use quantized export
        traced_model = model.convert_to_quantized_torchscript(input_spec)
    else:
        # regular export
        dummy_data = make_torch_inputs(input_spec)
        traced_model = torch.jit.trace(model, dummy_data)
    return traced_model


def get_target_model_size_and_parameters(model, input_spec):
    print("Running a compile job to get the target model's asset size.")
    job = hub.submit_compile_job(
        model=model, input_specs=input_spec, device=hub.Device("Samsung Galaxy S23")
    )
    job.wait()
    if job.get_status().success:
        with tempfile.TemporaryDirectory() as tmp_dirname:
            path = os.path.join(tmp_dirname, "model.tflite")
            job.download_target_model(path)
            size = get_checkpoint_file_size(path)
            parameters = get_tflite_unique_parameters(path)
            return size, parameters


def get_model_size_and_parameters(model):
    input_spec = model.get_input_spec()
    traced_model = trace_model(model, input_spec)
    size, parameters = get_target_model_size_and_parameters(traced_model, input_spec)
    return (size, parameters)


def add_details_to_info_yaml(info, details):
    for name, (size, parameters) in details.items():
        if "technical_details" in info:
            param_key = (
                "Number of parameters"
                if name == "model"
                else f"Number of parameters ({name})"
            )
            size_key = "Model size" if name == "model" else f"Model size ({name})"
            info["technical_details"][param_key] = parameters
            info["technical_details"][size_key] = size
    return info


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--models",
        "-m",
        nargs="+",
        type=str,
        default=None,
        help="Models for which to generate export.py.",
    )
    parser.add_argument(
        "--all",
        "-a",
        action="store_true",
        help="If set, generates files for all models.",
    )
    args = parser.parse_args()
    assert args.all or args.models, "Must specify -a or -m."
    if args.models:
        models = parser.parse_args().models
    else:
        models = get_all_models()

    for model_name in models:
        try:
            model_dir = get_qaihm_models_root() / model_name
            # Install dependencies
            requirements_file = None

            if (model_dir / "requirements.txt").exists():
                requirements_file = os.path.join(model_dir, "requirements.txt")
            if requirements_file:
                subprocess.run(["pip", "install", "-r", requirements_file])

            # imports the module from the given path
            model_module = importlib.import_module(
                f"qai_hub_models.models.{model_name}"
            )
            yaml = YAML()

            export_options = {}
            if (model_dir / "code-gen.yaml").exists():
                with open(model_dir / "code-gen.yaml", "r") as f:
                    export_options = yaml.load(f)

            details = dict()
            if "components" in export_options:
                model = model_module.Model.from_pretrained()
                for submodel_name, submodel in export_options["components"].items():
                    comp_model = eval(submodel)
                    details[submodel_name] = get_model_size_and_parameters(comp_model)

            else:
                model = model_module.Model.from_pretrained()
                details["model"] = get_model_size_and_parameters(model)

            if (model_dir / "info.yaml").exists():
                with open(model_dir / "info.yaml") as f:
                    info = yaml.load(f)
                    new_info = add_details_to_info_yaml(info=info, details=details)
                    with open(model_dir / "info.yaml", "wb") as f:
                        yaml.dump(new_info, f)
            else:
                new_info = add_details_to_info_yaml(info=dict(), details=details)
                with open(model_dir / "info.yaml", "w") as f:
                    yaml.dump(new_info, f)

            if requirements_file:
                subprocess.run(["pip", "uninstall", "-r", requirements_file])
        except Exception:
            print(traceback.format_exc())
            print(f"Not working {model_name}")


if __name__ == "__main__":
    main()
