import json
import paho.mqtt.client as mqtt
from config.config import CONFIG
from .utils import init_db, transform, validate, insert

# --- Config ---
BROKER = CONFIG["broker"]["host"]
PORT = CONFIG["broker"]["port"]
TOPIC = CONFIG["broker"]["topic"]


# -----------------------------------------------------------
# MQTT CALLBACKS
# -----------------------------------------------------------
def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print(f"[MQTT] Connected to broker at {BROKER}:{PORT}")
        client.subscribe(TOPIC)
        print(f"[MQTT] Subscribed to topic '{TOPIC}'")
    else:
        print(f"[MQTT] Connection failed with code {rc}")


def on_message(client, userdata, msg):
    print(f"\n[MQTT] Message received on '{msg.topic}'")

    try:
        payload = json.loads(msg.payload.decode("utf-8"))
    except json.JSONDecodeError as e:
        print(f"[MQTT] Failed to parse JSON: {e}")
        return

    payload = transform(payload)

    if not validate(payload):
        return

    insert(conn, payload)


if __name__ == "__main__":

    conn = init_db()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT)

    try:
        print("[MQTT] Listening... press Ctrl+C to stop")
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[MQTT] Stopped by user")
    finally:
        conn.close()
        print("[DB] Connection closed")