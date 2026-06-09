# Lab 6 - Serving API and MQTT Prediction

## Goal

In this lab, you use the registered model to predict fraud on incoming transactions.

The serving flow is:

```text
FastAPI starts
MQTT message arrives
transaction is transformed
model predicts fraud risk
transaction is saved
prediction is saved
```

## Files To Study

```text
src/serving/app.py
src/serving/model_loader.py
src/serving/predictor.py
src/serving/schemas.py
src/data_ingestion/utils.py
```

## Main Ideas

- FastAPI runs the service.
- `fastapi-mqtt` connects the service to MQTT.
- The app listens to the configured topic.
- The model is loaded from MLflow.
- Predictions are stored in the `predictions` table.

## Run

Start the main services:

```bash
docker compose up -d mqtt-broker mlflow
```

Run the serving API locally:

```bash
uvicorn src.serving.app:app --reload
```

Or run it with Docker Compose:

```bash
docker compose up --build serving-api
```

## Send A Transaction

Use the `/transaction` endpoint from the FastAPI docs:

```text
http://127.0.0.1:8000/docs
```

## Expected Result

The transaction is published to MQTT, processed by the app, predicted by the model, and stored in SQLite.
