import argparse
import importlib
import inspect
import json
import os
import random
import shutil
from pathlib import Path
from typing import List, Type

import boto3
import numpy as np
import torch
from botocore.client import BaseClient

from qai_hub_models.utils.base_model import BaseModel

try:
    from qai_hub_models.utils.quantization_aimet import AIMETQuantizableMixin
except NotImplementedError:
    # AIMET is not installed.
    AIMETQuantizableMixin = NotImplementedError  # type: ignore

REGISTERED_MODELS = [
    "mobilenet_v2",
    "trocr_encoder",
    "trocr_decoder",
]


AWS_PROFILE_VAR = "AWS_PROFILE"
BITSY_S3_BUCKET = "tetra-biz-data-bitsyfactory"
LOCAL_ASSETS_PATH = "build/zoo_to_bench_assets"


def get_s3_object(key: str) -> str:
    """
    Fetch s3 file and return the file contents as a string.
    """
    s3_client = S3ClientSingleton()
    response = s3_client.get_object(Bucket=BITSY_S3_BUCKET, Key=key)  # type: ignore
    return response["Body"].read().decode("utf-8")


class S3ClientSingleton:
    _instance = None

    def __new__(cls) -> BaseClient:
        if cls._instance is None:
            cls._instance = boto3.client("s3")
        return cls._instance


class AWSEnvManager:
    def __enter__(self):
        self.profile = os.environ.get(AWS_PROFILE_VAR, None)
        os.environ[AWS_PROFILE_VAR] = "tetra-biz-data"

    def __exit__(self, exc_type, exc_value, traceback):
        if self.profile is not None:
            os.environ[AWS_PROFILE_VAR] = "tetra-biz-data"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--models",
        type=str,
        required=True,
        help="Comma-separated list of models to update in bench. "
        "Each entry should map to one of the folders in qai_hub_models/folders. "
        "All models within the folder that subclass from QAI Hub Models, "
        "will have their assets generated."
        "For example `--models mobilenet_v2,trocr`",
    )
    parser.add_argument(
        "--skip-s3-upload",
        action="store_true",
        help="If set, model assets will only be written to disk, not uploaded to s3.",
    )
    return parser.parse_args()


def get_module(module_name: str):
    try:
        full_module_name = f"qai_hub_models.models.{module_name}.model"
        return importlib.import_module(full_module_name)
    except ModuleNotFoundError:
        pass

    try:
        full_module_name = f"qai_hub_models.models.internal.{module_name}.model"
        return importlib.import_module(full_module_name)
    except ModuleNotFoundError:
        raise ValueError(
            f"Unable to location model {module_name} in neither"
            "qai_hub_models.models.internal nor qai_hub_models.models\n"
        )


def get_module_names(args: argparse.Namespace) -> List[str]:
    modules = args.models.split(",")
    for module_name in modules:
        # Ensure each input module can be imported
        get_module(module_name)
    return modules


def get_models_for_module(module_name: str) -> List[str]:
    module = get_module(module_name)
    classes = inspect.getmembers(module, inspect.isclass)
    models = []
    for cls in classes:
        # Find all models defined in model.py
        if issubclass(cls[1], BaseModel) and cls[1].__module__ == module.__name__:
            models.append(cls[0])
    return models


def get_model_cls(model_name: str, module_name: str) -> Type[BaseModel]:
    module = get_module(module_name)
    return getattr(module, model_name)


def get_s3_path_prefix(model_name: str) -> str:
    return f"zoo-{model_name}/v"


def get_current_version(model_name: str) -> int:
    """
    Gets the max version present in the respective bitsy folder for each model.

    This takes precedence over what's in the local yaml file, since the local
    repo may be out of date, which may cause the script to accidentally override
    production assets.

    If the model is not present in s3 or the local .yaml,
    the model is omitted from the dict.
    """
    s3_client = S3ClientSingleton()
    version_prefix = get_s3_path_prefix(model_name)
    response = s3_client.list_objects_v2(  # type: ignore
        Bucket=BITSY_S3_BUCKET, Prefix=version_prefix, Delimiter="/"
    )
    max_version = 0
    for version_dir in response.get("CommonPrefixes", []):
        # Directory name will be like <version_prefix><version_number>/
        version = int(version_dir["Prefix"][len(version_prefix) : -1])
        max_version = max(version, max_version)
    return max_version


def write_bench_assets_to_disk(
    model_name: str,
    module_name: str,
) -> None:
    """
    For a given model, write the assets required by bench to disk. This is to prepare
    eventually uploading these assets to S3. The assets will be written to
    `build/zoo_to_bench_assets/<model_name>`.

    Before running, it will first delete anything that is currently in the folder.

    The folder will contain the following:

    - Traced model object
    - Sample input tensors
    - Input spec as json

    Parameters:
        model_name: Name of the Model to be imported
        module_name: Name of the subdirectory where the model lives, so it can be imported
    """
    output_dir = Path(LOCAL_ASSETS_PATH) / model_name.lower()
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # Need to set the seed to ensure reproducibility
    torch.manual_seed(42)
    random.seed(42)
    np.random.seed(42)
    model_cls = get_model_cls(model_name, module_name)
    model = model_cls.from_pretrained()
    assert isinstance(model, BaseModel)

    if isinstance(model, AIMETQuantizableMixin):
        try:
            model.convert_to_torchscript_and_aimet_encodings(
                str(output_dir), model_name=model_name
            )
        except Exception as e:
            print(
                f"Failed to convert {model_name} to AIMET torchscript + encodings: {str(e)}"
            )

        try:
            model.convert_to_onnx_and_aimet_encodings(
                str(output_dir), model_name=model_name
            )
        except Exception as e:
            print(f"Failed to convert {model_name} to AIMET ONNX + encodings: {str(e)}")

        torchscript_convert = model.convert_to_quantized_torchscript
    else:
        torchscript_convert = model.convert_to_torchscript

    try:
        torch.jit.save(torchscript_convert(), output_dir / "model.pth")
    except Exception as e:
        print(f"Failed to convert {model_name} to torchscript: {str(e)}")

    input_spec = model.get_input_spec()
    input_spec_json = json.dumps(input_spec, sort_keys=True)

    sample_inputs = {
        input_name: inputs[0] for input_name, inputs in model.sample_inputs().items()
    }

    np.savez(output_dir / "sample_inputs.npz", **sample_inputs)
    with open(output_dir / "input_spec.json", "w") as f:
        f.write(input_spec_json)


def push_assets_to_bitsy(model_name: str) -> None:
    """
    Push model assets from local disk to bitsy S3 bucket.

    Parameters:
        model_name: Name of the model to update.
        current_version: The latest version of bitsy assets that exit in S3.

    Returns:
        New version for the model assets.
    """
    s3_client = S3ClientSingleton()
    model_dir = Path(LOCAL_ASSETS_PATH) / model_name.lower()

    # Bump the version number before uploading uploading
    new_version = get_current_version(model_name) + 1
    s3_prefix = get_s3_path_prefix(model_name) + str(new_version)
    for file in model_dir.iterdir():
        s3_client.upload_file(  # type: ignore
            file.absolute(), BITSY_S3_BUCKET, f"{s3_prefix}/{file.name}"
        )


def update_model_assets(
    model_name: str,
    module_name: str,
    skip_s3: bool,
):
    """
    Main function for writing a model's assets to local disk and then
    pushing those assets to S3 if the hashes have changed.

    Parameters:
        model_name: Name of the Model to be imported
        module_name: Name of the subdirectory where the model lives, so it can be imported
        new_versions: dict of new_versions to be tracked across models, that later
            gets flushed to the local .yaml file.
    """
    write_bench_assets_to_disk(model_name, module_name)
    if not skip_s3:
        push_assets_to_bitsy(model_name)


def main() -> None:
    args = parse_args()
    module_names = get_module_names(args)

    for module_name in module_names:
        for model_name in get_models_for_module(module_name):
            update_model_assets(
                model_name,
                module_name,
                args.skip_s3_upload,
            )


if __name__ == "__main__":
    with AWSEnvManager():
        main()
