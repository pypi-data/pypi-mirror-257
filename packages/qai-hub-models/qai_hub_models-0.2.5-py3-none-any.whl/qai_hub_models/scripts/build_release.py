import argparse
import os
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

from ruamel.yaml import YAML

from qai_hub_models.scripts.generate_model_readme import generate_model_readme
from qai_hub_models.scripts.generate_summary_table import (
    generate_table,
    get_global_readme_path,
)
from qai_hub_models.utils.asset_loaders import (
    ASSET_BASES_DEFAULT_PATH,
    ASSET_CONFIG,
    ModelZooAssetConfig,
)
from qai_hub_models.utils.config_loaders import (
    MODEL_IDS,
    MODEL_STATUS,
    QAIHM_PACKAGE_ROOT,
    QAIHMModelInfo,
)
from qai_hub_models.utils.path_helpers import QAIHM_PACKAGE_NAME

QAIHM_ZOO_MODELS: List[QAIHMModelInfo] = [
    QAIHMModelInfo.from_model(id) for id in MODEL_IDS
]
PRIVATE_MODELS = [cfg for cfg in QAIHM_ZOO_MODELS if cfg.status == MODEL_STATUS.PRIVATE]
PUBLIC_MODELS = [cfg for cfg in QAIHM_ZOO_MODELS if cfg.status == MODEL_STATUS.PUBLIC]
FOLDER_NAME = "ai-hub-models-build"


def main():
    parser = argparse.ArgumentParser(
        description="Build release QAI Hub Models code.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        help="Path to output directory to dump QAI Hub Models code.",
    )
    args = parser.parse_args()

    # Verify correct environment variables are set.
    asset_cfg = ModelZooAssetConfig.load_asset_cfg(
        ASSET_BASES_DEFAULT_PATH, verify_env_has_all_variables=True
    )

    # Output folder
    output_folder = TemporaryDirectory()
    output_dir = Path(args.output_dir)
    output_root = Path(output_folder.name) / FOLDER_NAME

    # Verify output dir is valid
    if os.path.exists(output_dir / FOLDER_NAME):
        raise ValueError(f"{output_dir / FOLDER_NAME} already exists")

    # Copy repo root to tmp
    repo_dir = QAIHM_PACKAGE_ROOT.parent
    shutil.copytree(repo_dir, output_root)
    output_package_root = output_root / QAIHM_PACKAGE_NAME

    # Remove all untracked files
    subprocess.run(["git", "clean", "-dfx"], cwd=output_root)

    # Remove git
    shutil.rmtree(os.path.join(output_root, ".git"))

    # Remove gitignore
    os.remove(os.path.join(output_root, ".gitignore"))

    # Remove private models
    for model in PRIVATE_MODELS:
        shutil.rmtree(model.get_package_path(output_package_root))

    # Prepare public models
    for model in PUBLIC_MODELS:
        # If the model is missing a yaml, don't publish it
        if not os.path.exists(model.get_perf_yaml_path(output_package_root)):
            shutil.rmtree(model.get_package_path(output_package_root))
            continue

        # Write public readmes
        with open(model.get_readme_path(output_package_root), "w") as README:
            README.write(
                generate_model_readme(
                    model, model.has_model_requirements(output_package_root)
                )
            )

        # Remove code gen yaml
        if model.get_code_gen_yaml_path(output_package_root).exists():
            os.remove(model.get_code_gen_yaml_path(output_package_root))

        # Remove generated tests
        generated_tests = (
            model.get_package_path(output_package_root) / "test_generated.py"
        )
        if os.path.exists(generated_tests):
            os.remove(generated_tests)

    # Remove internal files
    shutil.rmtree(output_package_root / "scripts")
    shutil.rmtree(output_package_root / "models" / "internal")
    shutil.rmtree(output_package_root / "utils" / "internal")

    # Open asset bases, and overwrite with set env variables
    yaml = YAML()
    asset_bases_path = output_package_root / "asset_bases.yaml"
    os.remove(asset_bases_path)
    with open(asset_bases_path, "w") as f:
        yaml.dump(asset_cfg, f)

    # Open Global README
    readme_path = get_global_readme_path(output_root)
    with open(readme_path, "r") as global_readme:
        readme = global_readme.read()
    os.remove(readme_path)

    # Append README table
    readme += generate_table(PUBLIC_MODELS)

    # Set dynamic paths
    readme = readme.replace("{REPOSITORY_URL}", ASSET_CONFIG.repo_url)
    readme = readme.replace(
        "{REPOSITORY_ROOT_FILE_NAME}", ASSET_CONFIG.repo_url.split("/")[-1]
    )

    # Write to disk
    with open(readme_path, "w") as global_readme:
        global_readme.write(readme)

    # Copy QAI Hub Models to output dir
    shutil.move(str(output_root), str(output_dir))


if __name__ == "__main__":
    main()
