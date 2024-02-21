from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from qai_hub_models.utils.asset_loaders import ASSET_CONFIG
from qai_hub_models.utils.config_loaders import (
    MODEL_DOMAIN,
    MODEL_IDS,
    MODEL_USE_CASE,
    QAIHM_PACKAGE_NAME,
    QAIHM_PACKAGE_ROOT,
    QAIHMModelInfo,
)


def get_global_readme_path(root: Path):
    return root / "README.md"


TABLE_TITLE = (
    "| Model | README | Torch App | Device Export | CLI Demo\n| -- | -- | -- | -- | --"
)
TABLE_DIVIDER = "| | | | |"
subdomains: Dict[MODEL_DOMAIN, List[MODEL_USE_CASE]] = {
    MODEL_DOMAIN.COMPUTER_VISION: [
        MODEL_USE_CASE.IMAGE_CLASSIFICATION,
        MODEL_USE_CASE.IMAGE_EDITING,
        MODEL_USE_CASE.IMAGE_GENERATION,
        MODEL_USE_CASE.SUPER_RESOLUTION,
        MODEL_USE_CASE.SEMANTIC_SEGMENTATION,
        MODEL_USE_CASE.VIDEO_CLASSIFICATION,
        MODEL_USE_CASE.VIDEO_GENERATION,
        MODEL_USE_CASE.OBJECT_DETECTION,
        MODEL_USE_CASE.POSE_ESTIMATION,
        MODEL_USE_CASE.IMAGE_TO_TEXT,
    ],
    MODEL_DOMAIN.AUDIO: [
        MODEL_USE_CASE.SPEECH_RECOGNITION,
        MODEL_USE_CASE.AUDIO_ENHANCEMENT,
    ],
    MODEL_DOMAIN.MULTIMODAL: [],  # Anything is OK
    MODEL_DOMAIN.GENERATIVE_AI: [
        MODEL_USE_CASE.IMAGE_GENERATION,
        MODEL_USE_CASE.TEXT_GENERATION,
    ],
}


def main():
    """Generate a summary table for all models (including private ones) and append to the top level (repository) README."""
    with open(get_global_readme_path(QAIHM_PACKAGE_ROOT.parent), "a") as tl_readme:
        tl_readme.write(
            generate_table([QAIHMModelInfo.from_model(id) for id in MODEL_IDS])
        )


def get_title_divider(title: str) -> str:
    return f"{TABLE_DIVIDER}\n| **{title}**"


def get_model_entry(model: QAIHMModelInfo) -> str:
    return f"| [{model.name}]({ASSET_CONFIG.get_website_url(model.id, relative=False)}) | [{model.get_package_name()}]({model.get_readme_path(Path(QAIHM_PACKAGE_NAME))}) | ✔️ | ✔️ | ✔️"


def generate_table(models: List[QAIHMModelInfo]) -> str:
    """Constructs and returns a summarizing table of the provided models in markdown format.
    Generally, this table is used at the end of the top level README for the model zoo repository."""
    out = ""
    for domain in MODEL_DOMAIN:
        domain_models = [
            model_cfg for model_cfg in models if model_cfg.domain == domain
        ]
        if not domain_models:
            continue

        out = f"""{out}\

### {domain}

{TABLE_TITLE}
"""

        use_cases: List[MODEL_USE_CASE] = subdomains[domain]
        if not use_cases:
            # Dump everything into 1 table
            out = (
                f"{out}{TABLE_DIVIDER}\n"
                + "\n".join([get_model_entry(model) for model in domain_models])
                + "\n"
            )
        else:
            for use_case in use_cases:
                use_case_models = [
                    model for model in domain_models if model.use_case == use_case
                ]
                if use_case_models:
                    out = (
                        f"{out}{get_title_divider(str(use_case))}\n"
                        + "\n".join(
                            [get_model_entry(model) for model in use_case_models]
                        )
                        + "\n"
                    )
    return out


if __name__ == "__main__":
    main()
