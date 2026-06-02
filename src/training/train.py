import os

import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier

from config.config import CONFIG
from training.registry import register_best_model
from .preprocess import load_data, wrangle


MLFLOW_DB = f"sqlite:///{CONFIG['paths']['mlflow_db']}"
EXP_NAME = CONFIG["mlflow"]["experiment_name"]
ARTIFACT_PATH = f"file://{CONFIG['paths']['mlflow_artifacts']}"
MODEL_NAME = CONFIG["mlflow"]["model_name"]
RANDOM_STATE = CONFIG["train"]["random_state"]


def get_or_create_experiment(exp_name, artifact_location):
    """Get an existing MLflow experiment or create it if it does not exist."""
    experiment = mlflow.get_experiment_by_name(exp_name)
    if experiment is not None:
        return experiment

    experiment_id = mlflow.create_experiment(name=exp_name, artifact_location=artifact_location)
    return mlflow.get_experiment(experiment_id)


def split_features_target(df, target="isFraud"):
    X = df.drop(columns=[target])
    y = df[target]
    return X, y


def get_categorical_features(df):
    return df.select_dtypes("object").columns.tolist()


def split_train_test(X, y):
    return train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y,
    )


def build_model_pipeline(X_train, model_name):
    categorical_features = get_categorical_features(X_train)

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ],
        remainder="passthrough",
    )

    if model_name == "XGBClassifier":
        model = XGBClassifier(random_state=RANDOM_STATE, eval_metric="logloss")
    elif model_name == "RandomForestClassifier":
        model = RandomForestClassifier(random_state=RANDOM_STATE)
    else:
        raise ValueError(f"Unsupported model_name: {model_name}")

    return make_pipeline(preprocessor, model)


def tracking_experiment(run_name, registered_model_name, pipe, X_train, X_test, y_train, y_test):
    with mlflow.start_run(run_name=run_name):
        target_names = ["is_not_fraud", "is_fraud"]

        train_dataset = mlflow.data.from_pandas(X_train)
        mlflow.log_input(dataset=train_dataset, context="train")

        test_dataset = mlflow.data.from_pandas(X_test)
        mlflow.log_input(dataset=test_dataset, context="test")
        print("Dataset logged.")

        pipe.fit(X_train, y_train)

        y_train_pred = pipe.predict(X_train)
        y_test_pred = pipe.predict(X_test)

        accuracy_train = pipe.score(X_train, y_train)
        accuracy_test = pipe.score(X_test, y_test)
        f1_train = f1_score(y_train, y_train_pred)
        f1_test = f1_score(y_test, y_test_pred)

        mlflow.log_metrics(
            {
                "accuracy_train": round(accuracy_train, 4),
                "f1_score_train": round(f1_train, 4),
                "accuracy_test": round(accuracy_test, 4),
                "f1_score_test": round(f1_test, 4),
            }
        )

        print("Training score", accuracy_train)
        print("F1 score training", f1_train)
        print("Test score", accuracy_test)
        print("F1 score test", f1_test)
        print(classification_report(y_true=y_test, y_pred=y_test_pred, target_names=target_names))
        print("Metrics logged.")

        mlflow.sklearn.log_model(pipe, artifact_path=registered_model_name)
        print("Model logged.")

        cm = confusion_matrix(y_true=y_test, y_pred=y_test_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=target_names)
        disp.plot()
        mlflow.log_figure(disp.figure_, f"confusion_matrix_{run_name}.png")
        plt.close(disp.figure_)
        print("Confusion matrix logged.")


def run_models(X_train, X_test, y_train, y_test):
    tracking_experiment(
        "xgboost",
        MODEL_NAME,
        build_model_pipeline(X_train, model_name="XGBClassifier"),
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
    )
    tracking_experiment(
        "random_forest",
        MODEL_NAME,
        build_model_pipeline(X_train, model_name="RandomForestClassifier"),
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
    )



def main():
    #create if not exists.
    os.makedirs(os.path.dirname(CONFIG["paths"]["mlflow_db"]), exist_ok=True)
    os.makedirs(CONFIG["paths"]["mlflow_artifacts"], exist_ok=True)

    mlflow.set_tracking_uri(MLFLOW_DB)
    experiment = get_or_create_experiment(EXP_NAME, ARTIFACT_PATH)
    mlflow.set_experiment(experiment.name)

    wrangled_df = wrangle(load_data())
    X, y = split_features_target(wrangled_df, target="isFraud")
    X_train, X_test, y_train, y_test = split_train_test(X, y)

    run_models(X_train, X_test, y_train, y_test)
    register_best_model(EXP_NAME, MODEL_NAME)


if __name__ == "__main__":
    main()
