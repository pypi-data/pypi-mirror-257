from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path
from typing import List

import yaml
from jinja2 import Environment, FileSystemLoader

from qai_hub_models.utils.args import DEFAULT_EXPORT_DEVICE
from qai_hub_models.utils.config_loaders import QAIHMModelInfo
from qai_hub_models.utils.path_helpers import get_all_models, get_qaihm_models_root

HEADER = "# THIS FILE WAS AUTO-GENERATED. DO NOT EDIT MANUALLY."


def _generate_export(
    environment, model_name, model_display_name, export_options, model_dir
):
    template = environment.get_template("export_template.txt")
    file_contents = template.render(
        export_options,
        model_name=model_name,
        model_display_name=model_display_name,
        header=HEADER,
        device=DEFAULT_EXPORT_DEVICE,
    )
    export_file_path = os.path.join(model_dir, "export.py")
    with open(export_file_path, "w") as f:
        f.write(file_contents)
    return export_file_path


def _generate_unit_tests(environment, model_name, export_options, model_dir):
    original_test_path = model_dir / "test.py"
    new_test_path = model_dir / "test_generated.py"
    with open(original_test_path, "r") as f:
        original_file_contents = f.read()
    skip_clone_repo = "skip_clone_repo_check" in original_file_contents
    template = environment.get_template("unit_test_template.txt")
    file_contents = template.render(
        export_options,
        model_name=model_name,
        skip_clone_repo=skip_clone_repo,
        header=HEADER,
    )

    with open(new_test_path, "w") as f:
        f.write(file_contents)
    return new_test_path


def generate_export_file(model_name: str) -> List[str]:
    model_dir = get_qaihm_models_root() / model_name
    export_options = {}
    if (model_dir / "code-gen.yaml").exists():
        with open(model_dir / "code-gen.yaml", "r") as f:
            export_options = yaml.safe_load(f)

    if export_options.get("no_assets", False):
        print(f"Skipping export.py generation for {model_name}.")
        return []

    try:
        model_info = QAIHMModelInfo.from_model(model_name)
        model_display_name = model_info.name
    except ValueError:
        # Info yaml does not exist
        model_display_name = "no_info_yaml_found"

    environment = Environment(
        loader=FileSystemLoader(Path(__file__).parent / "templates/"),
        keep_trailing_newline=True,
    )

    generated_files = [
        _generate_export(
            environment, model_name, model_display_name, export_options, model_dir
        )
    ]
    skip_tests = export_options.get("skip_tests", False)
    if not skip_tests:
        generated_files.append(
            _generate_unit_tests(environment, model_name, export_options, model_dir)
        )

    zoo_root = get_qaihm_models_root()
    return [os.path.join(zoo_root, gen_file) for gen_file in generated_files]


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
    modified_files = []
    for model in models:
        modified_files.extend(generate_export_file(model))
    os.environ["SKIP"] = "mypy"
    subprocess.run(["pre-commit", "run", "--files"] + modified_files)


if __name__ == "__main__":
    main()
