import os

from qai_hub_models.utils.config_loaders import (
    MODEL_IDS,
    MODEL_STATUS,
    QAIHMModelInfo,
    QAIHMModelPerf,
)


def main():
    """Generate a summary to showcase which models are not public and issues with public marked models."""
    private_models = []
    propreitary_models = []
    no_perf_yamls = []
    no_good_perf_both = []
    no_good_tflite = []
    total = []
    for model_id in MODEL_IDS:
        total.append(model_id)
        model_info = QAIHMModelInfo.from_model(model_id)
        model_perf = QAIHMModelPerf(perf_yaml_path=model_info.get_perf_yaml_path())

        if model_info.status == MODEL_STATUS.PRIVATE:
            private_models.append(model_id)

        elif model_info.status == MODEL_STATUS.PROPRIETARY:
            propreitary_models.append(model_id)

        else:
            if not os.path.exists(model_info.get_perf_yaml_path()):
                no_perf_yamls.append(model_id)
            else:
                if model_perf.skip_overall:
                    no_good_perf_both.append(model_id)
                else:
                    if model_perf.skip_overall:
                        no_good_tflite.append(model_id)

    print("Summary of models to be published.")
    print("==================================")
    print(f"Models marked private : {len(private_models)}")
    print(private_models)
    print(f"Models markes propreitary (GEN AI): {len(propreitary_models)}")
    print(propreitary_models)
    public = len(total) - len(private_models) - len(propreitary_models)
    print(f"Models marked public: {public}")
    print("----------------------------")
    print(f"Public marked models without perf.yaml: {len(no_perf_yamls)}")
    print(no_perf_yamls)
    print(
        f"Public marked models with perf marked null on TFLite/QNN: {len(no_good_perf_both)} "
    )
    print(no_good_perf_both)
    print(
        f"Public marked models with perf marked null on TFLite: {len(no_good_tflite)}"
    )
    print(no_good_tflite)


if __name__ == "__main__":
    main()
