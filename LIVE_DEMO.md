## Demo Goal

Full MLOps flow:

```text
transaction data -> MQTT ingestion -> SQLite -> training -> MLflow -> model registry -> serving API -> predictions -> Grafana -> monitoring -> orchestration -> Docker/CI
```

## 1. Project Structure [each folder is one MLOps responsibility]

```text
config/
data/
src/data_ingestion/
src/training/
src/serving/
src/monitoring/
src/orchestration/
docker-compose.yml
.github/workflows/ci.yml
Visuals.md
```

## 2. Start The Core Services

Run:

```bash
docker compose up -d mqtt-broker mlflow grafana
```


```bash
docker compose ps
```

## 4. Data Ingestion

Run the subscriber in one terminal:

```bash
python3 -m src.data_ingestion.subscriber
```

Run the publisher in another terminal:

```bash
python3 -m src.data_ingestion.publisher
```

---------



```text
publisher.py -> MQTT broker -> subscriber.py -> data/transactions.db
```

Stop both with:

```text
Ctrl+C
```

## 5. The SQLite Tables

Explain:

```text
transactions table = what happened
predictions table = what the model decided
```

Optional command:

```bash
sqlite3 data/transactions.db ".tables"
```

Optional command:

```bash
sqlite3 data/transactions.db "SELECT transactionID, type, amount, datetime FROM transactions LIMIT 5;"
```

## 6. Training

Training loads the data, prepares it, trains candidate models, evaluates them, and logs everything to MLflow.

```text
src/training/preprocess.py
src/training/train.py
src/training/registry.py
```


Run:

```bash
python3 -m src.training.train
```


## 7. MLflow

Open:

```text
http://127.0.0.1:5123
```


```text
experiment
XGBoost run
RandomForest run
f1_score_test
confusion matrix artifact
registered model
```


MLflow keeps track of what we trained, how it performed, and which model version we can serve.


## 8. Serving API

Start the API:

```bash
uvicorn src.serving.app:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```


```text
/health
/transaction
```

The trained model is now available through an API.


## 9. Send A Transaction

Use the `/transaction` endpoint in FastAPI docs.

Example payload:

```json
{
  "type": "TRANSFER",
  "amount": 10000,
  "nameOrig": "C123456",
  "oldbalanceOrg": 10000,
  "newbalanceOrig": 0,
  "nameDest": "C987654",
  "oldbalanceDest": 0,
  "newbalanceDest": 10000,
  "datetime": "2026-07-18 10:00:00",
  "transactionID": "demo-transaction-001"
}
```


The API publishes the transaction to MQTT. The app receives it, transforms it, predicts fraud risk, then stores the transaction and prediction.


## 10. Prediction Storage

Optional command:

```bash
sqlite3 data/transactions.db "SELECT transactionID, prediction, fraud_probability, risk_level, predicted_at FROM predictions ORDER BY predicted_at DESC LIMIT 5;"
```


This prediction table gives us audit history. We can see what the model decided and when.


## 11. Grafana

Open:

```text
http://127.0.0.1:3123
```

Show panels like:

```text
total transactions
total predictions
risk level breakdown
high-risk percentage
latest predictions
transaction volume by type
```


Grafana makes the system visible. It helps us understand what is happening after predictions are made.


## 12. Show Monitoring

Run:

```bash
python3 -m src.monitoring.drift
```

Open:

```text
reports/drift_report.html
```


Monitoring compares current transaction data with the original training data. This helps us know when the data starts changing.


## 13. Show Orchestration



```text
src/orchestration/flows.py
```

Run:

```bash
python3 -m src.orchestration.flows
```


Prefect lets us organize repeatable jobs like training and monitoring into one workflow.


## 14. Docker And CI/CD



```text
Dockerfile
docker-compose.yml
.github/workflows/ci.yml
```


Docker packages the project. Docker Compose runs the local services. GitHub Actions builds and publishes the image.




## Quick Troubleshooting

If port `1883` is busy:

```bash
docker compose stop mqtt-broker
```

If MLflow is not opening:

```bash
docker compose up -d mlflow
```

If the serving API cannot predict:

```text
Make sure a model has already been trained and registered in MLflow.
```

If Grafana has no data:

```text
Run ingestion and send at least one transaction through the API.
```

If Evidently fails:

```text
Make sure data/transactions.db contains ingested transactions.
```
