from sklearn.metrics import  f1_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from xgboost import XGBClassifier
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import warnings

from config.config import CONFIG
import mlflow
import os

from training.preprocess import load_data, wrangle

MLFLOW_DB = f"sqlite:///{CONFIG['paths']['mlflow_db']}"
EXP_NAME = CONFIG["mlflow"]["experiment_name"]
ARTIFACT_PATH = f"file://{CONFIG['paths']['mlflow_artifacts']}"

MODEL_NAME = CONFIG["mlflow"]["model_name"]

RANDOM_STATE = CONFIG["train"]["random_state"]

def get_or_create_experiment(exp_name, artifact_location):
    """Get existing experiment by name or create a new one if it doesn't exist."""
    experiment = mlflow.get_experiment_by_name(exp_name)
    if experiment is not None:
        print(f"Experiment '{exp_name}' already exists (ID: {experiment.experiment_id})")
        return experiment

    print(f"Creating new experiment '{exp_name}' with artifact location '{artifact_location}'")
    experiment_id = mlflow.create_experiment(name=exp_name, artifact_location=artifact_location)
    return mlflow.get_experiment(experiment_id)

def split_features_target(df, target="isFraud"):
    X = df.drop(columns=[target])
    y = df[target]
    return X, y


def get_categorical_features(df):
    return df.select_dtypes("object").columns.tolist()



def split_train_test( X, y):
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )
    return X_train, X_test, y_train, y_test


def tracking_expirement(run_name, model_name, pipe, X_test, X_train, y_test, y_train):
    with mlflow.start_run(run_name=run_name):
        
        target_names = ["is_not_fraud", "is_fraud"]

        # ***************Log dataset**************************
        
        test_dataset = mlflow.data.from_pandas(X_test)
        mlflow.log_input(dataset=test_dataset, context="test")

        train_dataset = mlflow.data.from_pandas(X_train)
        mlflow.log_input(dataset=train_dataset, context="train")

        print("Dataset Logged !")
        # *************** Log metrics **************************
        
        pipe.fit(X_train, y_train)


        accurary = pipe.score(X_train, y_train)
        f1_metric = f1_score(y_train, pipe.predict(X_train))

        accurary_test = pipe.score(X_test, y_test)
        f1_metric_test = f1_score(y_test, pipe.predict(X_test))

        mlflow.log_metrics({
            "accuracy_train": round(accurary, 2),
            "f1_score_train": round(f1_metric,2) ,
            "accuracy_test": round(accurary_test,2),
            "f1_score_test": round(f1_metric_test,2)
        })

        print("Training score", accurary)
        print("F1 score training", f1_metric)

        print("Test score", accurary_test)
        print("F1 score test", f1_metric_test)

        print(classification_report(y_true=y_test, y_pred=pipe.predict(X_test), target_names=target_names))
       
        print("Metrics logged !")
        # *************** Log model **************************

        mlflow.sklearn.log_model(pipe, name=model_name)
        print("Model Logged !")

        cm = confusion_matrix(y_true=y_test, y_pred=pipe.predict(X_test))
        disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                    display_labels=target_names)
        disp.plot()

        # *************** Log figure **************************

        mlflow.log_figure(disp.figure_, f"confusion_matrix_{model_name}.png")
        print("Confusion matrix logged !")


def train_model(df, model_name="XGBClassifier"):   

    categorical_features = get_categorical_features(df)

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
        ],
        remainder="passthrough"
    )

    return make_pipeline(
        preprocessor,
        XGBClassifier() if model_name == "XGBClassifier" else RandomForestClassifier()
    )

        

def run_models(df,X_train, X_test, y_train, y_test):
    tracking_expirement("xgboost", MODEL_NAME, train_model(df, model_name="XGBClassifier"), X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)
    tracking_expirement("random_forest", MODEL_NAME, train_model(df, model_name="RandomForestClassifier"), X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)


def register_best_model(experiment_name, model_name):

    # Get experiment by name
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        raise ValueError(f"Experiment '{experiment_name}' not found")

    # Search all runs in the experiment, ordered by f1_score_test descending
    best_run = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.f1_score_test DESC"],
        max_results=1
    )

    if best_run.empty:
        raise ValueError(f"No runs found in experiment '{experiment_name}'")

    best_run_id = best_run.iloc[0]["run_id"]
    best_run_name = best_run.iloc[0]["tags.mlflow.runName"]
    best_f1    = best_run.iloc[0]["metrics.f1_score_test"]

    print(f"Best run ID : {best_run_id}")
    print(f"Best F1 test: {best_f1:.4f}")

    # Register the model from the best run
    model_uri = f"runs:/{best_run_id}/{model_name}"
    registered = mlflow.register_model(model_uri=model_uri, name=model_name)

    client = mlflow.tracking.MlflowClient()
    client.set_model_version_tag(
        name=model_name,
        version=registered.version,
        key="run_name",
        value=best_run_name
    )

    print(f"Model '{model_name}' registered — version {registered.version}")
    print(f"Tagged with run_name: {best_run_name}")
    return registered



# mlflow implementation
mlflow.set_tracking_uri(MLFLOW_DB)
experiment = get_or_create_experiment(EXP_NAME, ARTIFACT_PATH)
mlflow.set_experiment(experiment.name)

wrangled_df = wrangle(load_data())



X,y = split_features_target(wrangled_df, target="isFraud")

X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

run_models(wrangled_df, X_train, X_test, y_train, y_test)
register_best_model(EXP_NAME, MODEL_NAME)

 