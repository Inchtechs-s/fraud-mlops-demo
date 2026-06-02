

import mlflow

from config.config import CONFIG


def register_best_model(experiment_name, model_name):

    MIN_F1_SCORE = CONFIG["train"]["min_f1_score"]
    experiment = mlflow.get_experiment_by_name(experiment_name)

    best_run = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.f1_score_test DESC"],
        max_results=1,
    )

    best_run_id = best_run.iloc[0]["run_id"]
    best_run_name = best_run.iloc[0]["tags.mlflow.runName"]
    best_f1 = best_run.iloc[0]["metrics.f1_score_test"]


    #if model is below our threshold score, let us just skip it.
    if best_f1 < MIN_F1_SCORE:
        print(
            f"Best model not registered. "
            f"F1 score {best_f1:.4f} is below threshold {MIN_F1_SCORE:.4f}."
        )
        return None
    
    print(f"Best run ID : {best_run_id}")
    print(f"Best F1 test: {best_f1:.4f}")

    model_uri = f"runs:/{best_run_id}/{model_name}"
    registered = mlflow.register_model(model_uri=model_uri, name=model_name)

    client = mlflow.tracking.MlflowClient()
    client.set_model_version_tag(
        name=model_name,
        version=registered.version,
        key="run_name",
        value=best_run_name,
    )

    print(f"Model '{model_name}' registered - version {registered.version}")
    print(f"Tagged with run_name: {best_run_name}")
    return registered