from datetime import datetime

import pandas as pd

from config.config import CONFIG
from .model_loader import load_latest_model
from .schemas import TransactionRequest


MODEL_NAME = CONFIG["mlflow"]["model_name"]

_MODEL = None
_MODEL_VERSION = None


def get_model():
    global _MODEL, _MODEL_VERSION

    if _MODEL is None:
        _MODEL, _MODEL_VERSION = load_latest_model()

    return _MODEL, _MODEL_VERSION


def _extract_time(transaction: TransactionRequest):
    #in case still step
    if transaction.step is not None:
        return (transaction.step - 1) % 24 + 1

    #in case datetime.
    if transaction.datetime:
        parsed = datetime.strptime(transaction.datetime, "%Y-%m-%d %H:%M:%S")
        return parsed.hour + 1

    return 1


def build_feature_frame(transaction: TransactionRequest):
    return pd.DataFrame(
        [
            {
                "type": transaction.type,
                "amount": transaction.amount,
                "nameOrig": transaction.nameOrig[0],
                "oldbalanceOrg": transaction.oldbalanceOrg,
                "nameDest": transaction.nameDest[0],
                "oldbalanceDest": transaction.oldbalanceDest,
                "time": _extract_time(transaction),
            }
        ]
    )


def risk_level(fraud_probability):
    if fraud_probability is None:
        return "unknown"
    if fraud_probability >= 0.8:
        return "high"
    if fraud_probability >= 0.5:
        return "medium"
    return "low"


def predict_transaction(transaction: TransactionRequest):
    model, version = get_model()
    features = build_feature_frame(transaction)

    prediction = int(model.predict(features)[0])
    fraud_probability = None

    predict_proba = getattr(model, "predict_proba", None)
    if predict_proba is not None:
        probabilities = predict_proba(features)
        fraud_probability = float(probabilities[0][1])

    return {
        "transactionID": transaction.transactionID,
        "prediction": prediction,
        "fraud_probability": fraud_probability,
        "risk_level": risk_level(fraud_probability),
        "model_name": MODEL_NAME,
        "model_version": str(version.version),
    }
