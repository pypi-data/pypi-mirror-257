import os

import yaml

from qai_hub_models.utils.config_loaders import ASSET_CONFIG, MODEL_IDS, QAIHMModelInfo

README_TEMPLATE = open(
    os.path.join(os.path.dirname(__file__), "templates", "model_readme_template.md")
).read()

NO_LICENSE = "This model's original implementation does not provide a LICENSE."


def main():
    """Generate a README for each model, and save it in <model_dir>/README.md."""
    for model_id in MODEL_IDS:
        model_info = QAIHMModelInfo.from_model(model_id)
        readme = generate_model_readme(model_info, model_info.has_model_requirements())
        readme_path = model_info.get_readme_path()
        if os.path.exists(readme_path):
            os.remove(readme_path)
        with open(readme_path, "w") as readme_file:
            readme_file.write(readme)


def _get_package_instructions(model_id: str):
    return f"""
Install the package via pip:
```bash
pip install \"qai_hub_models[{model_id}]\"
```
"""


def _get_example_and_usage_section(
    package_install_instructions: str, model_package: str
):
    return f"""
## Example & Usage
{package_install_instructions}

Once installed, run the following simple CLI demo:

```bash
python -m {model_package}.demo
```
More details on the CLI tool can be found with the `--help` option. See
[demo.py](demo.py) for sample usage of the model including pre/post processing
scripts. Please refer to our [general instructions on using
models](../../#qai-hub-models) for more usage instructions.

## Export for on-device deployment

This repository contains export scripts that produce a model optimized for
on-device deployment. This can be run as follows:

```bash
python -m {model_package}.export
```
Additional options are documented with the `--help` option. Note that the above
script requires access to Deployment instructions for Qualcomm® AI Hub."""


def generate_model_readme(
    model_info: QAIHMModelInfo, needs_install_instructions: bool
) -> str:
    """Generate a README for this model from the template found at .model_readme_template.md"""
    # Replace placeholders
    readme = README_TEMPLATE

    model_code_gen = {}
    model_code_gen_path = model_info.get_code_gen_yaml_path()
    if os.path.exists(model_code_gen_path):
        with open(model_code_gen_path, "r") as f:
            model_code_gen = yaml.safe_load(f)

    has_assets = not model_code_gen.get("no_assets", False)

    package_installation = (
        _get_package_instructions(model_info.id) if needs_install_instructions else ""
    )
    example_and_usage = _get_example_and_usage_section(
        package_installation, model_info.get_package_name()
    )
    for placeholder, replacement in [
        ["{model_id}", model_info.id],
        ["{example_and_usage}", example_and_usage if has_assets else ""],
        ["{model_name}", model_info.name],
        [
            "{model_url}",
            f"{ASSET_CONFIG.models_website_url}/models/{model_info.id}",
        ],
        ["{model_headline}", model_info.headline.strip(".")],
        ["{model_description}", model_info.description],
        ["{research_paper_title}", model_info.research_paper_title],
        ["{research_paper_url}", model_info.research_paper],
        ["{source_repo}", model_info.source_repo],
        [
            "{license_url}",
            model_info.license
            if model_info.license.casefold() != "none"
            else NO_LICENSE,
        ],
    ]:
        readme = readme.replace(placeholder, replacement)
    return readme


if __name__ == "__main__":
    main()
