import os
import yaml

# project root (parent of src/ which is the parent of common/)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# full config path
CONFIG_PATH = os.path.join(ROOT_DIR, 'config/config.yml')


def get_full_path(rel_path):
    return os.path.normpath(os.path.join(ROOT_DIR, rel_path))


def resolve_paths(obj):
    """
    Recursively convert all relative paths inside the config
    to absolute paths based on ROOT_DIR.
    """
    if isinstance(obj, dict):
        return {k: resolve_paths(v) for k, v in obj.items()}

    if isinstance(obj, str):
        return get_full_path(obj)

    return obj

with open(CONFIG_PATH, "r") as f:
    CONFIG = yaml.safe_load(f)


CONFIG["paths"] = resolve_paths(CONFIG["paths"])


def apply_env_overrides(config):
    """Allow Docker services to override local config values."""
    broker_host = os.getenv("FRAUD_BROKER_HOST")
    broker_port = os.getenv("FRAUD_BROKER_PORT")
    mlflow_uri = os.getenv("FRAUD_MLFLOW_URI")

    if broker_host:
        config["broker"]["host"] = broker_host

    if broker_port:
        config["broker"]["port"] = int(broker_port)

    if mlflow_uri:
        config["mlflow"]["uri"] = mlflow_uri


apply_env_overrides(CONFIG)
