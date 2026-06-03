# from fastapi import FastAPI, HTTPException
# from flask import json

# from config.config import CONFIG
# from data_ingestion.utils import init_db, insert, transform, validate
# from .model_loader import get_latest_model_version
# from .predictor import predict_transaction
# from .schemas import PredictionResponse, TransactionRequest


# app = FastAPI(title="Fraud Detection API")


# @app.get("/health")
# def health():
#     return {"status": "ok"}


# @app.get("/model/info")
# def model_info():
#     try:
#         version = get_latest_model_version()
#     except RuntimeError as exc:
#         raise HTTPException(status_code=503, detail=str(exc)) from exc

#     return {
#         "model_name": CONFIG["mlflow"]["model_name"],
#         "model_version": version.version,
#         "run_id": version.run_id,
#     }


# @app.post("/predict", response_model=PredictionResponse)
# def predict(transaction: TransactionRequest):
#     try:
#         return predict_transaction(transaction)
#     except RuntimeError as exc:
#         raise HTTPException(status_code=503, detail=str(exc)) from exc
#     except ValueError as exc:
#         raise HTTPException(status_code=400, detail=str(exc)) from exc


from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_mqtt.config import MQTTConfig
from fastapi_mqtt.fastmqtt import FastMQTT

from config.config import CONFIG
import json
from src.data_ingestion.utils import init_db, init_db_predictions, init_db_transactions, insert, insert_prediction, transform, validate
from .predictor import predict_transaction
from .schemas import TransactionRequest



# --- Config ---
BROKER = CONFIG["broker"]["host"]
PORT = CONFIG["broker"]["port"]
TOPIC = CONFIG["broker"]["topic"]


fast_mqtt = FastMQTT(config=MQTTConfig(
    host=BROKER,
    port=PORT,
 ))

@asynccontextmanager
async def _lifespan(app: FastAPI):
    app.state.conn_transactions = init_db_transactions()
    app.state.conn_predictions = init_db_predictions()

    await fast_mqtt.mqtt_startup()

    yield

    await fast_mqtt.mqtt_shutdown()
    app.state.conn_transactions.close()
    app.state.conn_predictions.close()


app = FastAPI(lifespan=_lifespan)

@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    if rc == 0:
        print(f"[MQTT] Connected to broker at {BROKER}:{PORT}")
        fast_mqtt.client.subscribe(TOPIC)
        print(f"[MQTT] Subscribed to topic '{TOPIC}'")
    else:
        print(f"[MQTT] Connection failed with code {rc}")

# @fast_mqtt.on_message()
# async def message(client, topic, payload, qos, properties):
#     print("Received message: ",topic, payload.decode(), qos, properties)
#     return 0

@fast_mqtt.subscribe(TOPIC)
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)
    print(f"\n[MQTT] Message received on '{topic}'")

    try:
        payload = json.loads(payload.decode("utf-8"))
    except json.JSONDecodeError as e:
        print(f"[MQTT] Failed to parse JSON: {e}")
        return

    payload = transform(payload)

    if not validate(payload):
        return

    try:
        predicted_transaction_outcome = predict_transaction(transaction=TransactionRequest(**payload))
    except RuntimeError as exc:
        print(f"[PREDICTION] Prediction failed: {exc}")
        return
    
    insert(app.state.conn_transactions, payload)

    match predicted_transaction_outcome["risk_level"]:
        case "low" | "unknown":
            print(f"[PREDICTION] Transaction {payload['transactionID']} is low risk or unknown.")
   
        case "medium":
            print(f"[PREDICTION] Transaction {payload['transactionID']} is medium risk.")
            
        case "high":
            print(f"[PREDICTION] Transaction {payload['transactionID']} is high risk.")
            print(f"[ALERT] Transaction {payload['transactionID']} flagged for review!")
    
    insert_prediction(app.state.conn_predictions, predicted_transaction_outcome)

@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("[MQTT] Disconnected")

@fast_mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("[MQTT] Subscribed", client, mid, qos, properties)


@app.post("/transaction")
async def receive_transaction(transaction: TransactionRequest):
    fast_mqtt.publish(TOPIC, json.dumps(transaction.model_dump())) #publishing mqtt topic
    return {"result": True,"message":"Transaction initiated, Processing in progress" }


@app.get("/health")
def health():
    return {"status": "ok"}
