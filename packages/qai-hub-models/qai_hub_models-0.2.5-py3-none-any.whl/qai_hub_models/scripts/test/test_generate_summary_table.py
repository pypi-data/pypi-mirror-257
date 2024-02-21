import os

from qai_hub_models.scripts.generate_summary_table import generate_table
from qai_hub_models.scripts.generate_summary_table import subdomains as domains_map
from qai_hub_models.utils.config_loaders import (
    ASSET_CONFIG,
    MODEL_DOMAIN,
    MODEL_USE_CASE,
    QAIHMModelInfo,
)

TEST_MODELS = ["resnet_mixed", "trocr", "yolov7"]


def test_all_domains_accounted_for():
    # Verify all use cases and domains are accounted for in the mapping
    assert len(domains_map) == len(MODEL_DOMAIN)
    use_cases = set([ucase for ucases in domains_map.values() for ucase in ucases])
    assert len(use_cases) == len(MODEL_USE_CASE)


def test_gen_summary_table():
    # Verify summary table looks as expected with sample models
    table = generate_table(
        [QAIHMModelInfo.from_model(model_id) for model_id in TEST_MODELS]
    )
    expected = open(
        os.path.join(os.path.dirname(__file__), "summary_table_expected.md")
    ).read()

    # Use currently configured repo url
    expected = expected.replace("{QAIHM_WEBSITE_URL}", ASSET_CONFIG.models_website_url)

    assert table == expected
