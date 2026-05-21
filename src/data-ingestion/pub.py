import paho.mqtt.client as mqtt
from config.config import CONFIG
import uuid
import pandas as pd
import time
import json

# --- Config ---
BROKER = CONFIG["broker"]["host"]
PORT = CONFIG["broker"]["port"]
TOPIC = CONFIG["broker"]["topic"]
DATA = CONFIG["paths"]["data"]
INTERVAL = CONFIG["broker"]["interval"]

# --- Load data ---
df = pd.read_pickle(DATA)
df = df.drop(columns=["step", "isFraud", "isFlaggedFraud"])
print(f"Loaded {len(df)} rows from {DATA}")

# --- MQTT Client ---
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)
client.loop_start()

# --- Publish one sample every 30s ---
for i, (_, row) in enumerate(df.iterrows()):
    payload = row.to_dict()

    # Convert non-serializable types (e.g. numpy int64, float32)
    payload = {k: (v.item() if hasattr(v, "item") else v) for k, v in payload.items()}
    payload["datetime"] = time.strftime("%Y-%m-%d %H:%M:%S")
    payload["transactionID"] =  str(uuid.uuid4())

    message = json.dumps(payload)
    result = client.publish(TOPIC, message)

    print(f"[{i+1}/{len(df)}] Published transaction ID {payload.get('TransactionID', i)}: {result}")

    time.sleep(INTERVAL)

client.loop_stop()
client.disconnect()
print("Done.")