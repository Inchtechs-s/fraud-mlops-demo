from typing import Literal

from pydantic import BaseModel, Field


TransactionType = Literal["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]


class TransactionRequest(BaseModel):
    transactionID: str
    type: TransactionType
    amount: float = Field(gt=0)
    nameOrig: str
    oldbalanceOrg: float = Field(ge=0)
    newbalanceOrig: float = Field(ge=0)
    nameDest: str
    oldbalanceDest: float = Field(ge=0)
    newbalanceDest: float = Field(ge=0)
    datetime: str | None = None
    step: int | None = Field(default=None, ge=1)


class PredictionResponse(BaseModel):
    transactionID: str
    prediction: int
    fraud_probability: float | None
    risk_level: str
    model_name: str
    model_version: str
