import mlflow
import mlflow.sklearn

from config.config import CONFIG


TRACKING_URI = f"sqlite:///{CONFIG['paths']['mlflow_db']}"
MODEL_NAME = CONFIG["mlflow"]["model_name"]


def get_latest_model_version(model_name=MODEL_NAME):
    mlflow.set_tracking_uri(TRACKING_URI)
    client = mlflow.tracking.MlflowClient()
    versions = client.search_model_versions(f"name = '{model_name}'")

    if not versions:
        raise RuntimeError(f"No registered versions found for model '{model_name}'")

    return max(versions, key=lambda version: int(version.version))


def load_latest_model(model_name=MODEL_NAME):
    version = get_latest_model_version(model_name)
    model_uri = f"models:/{model_name}/{version.version}"
    model = mlflow.sklearn.load_model(model_uri)
    return model, version
