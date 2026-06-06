import paho.mqtt.client as mqtt

# --- Config ---
# TODO: Fill in the same broker, port and topic as your publisher

BROKER = ""       # e.g. "test.mosquitto.org"
PORT   = 0       # e.g. 1883
TOPIC  = ""       # must match the publisher topic exactly


# --- Callbacks ---
def on_connect(client, userdata, flags, rc):
    # TODO: Print a confirmation message if rc == 0

    # TODO: Subscribe to TOPIC (hint: client.subscribe)
    pass


def on_message(client, userdata, msg):
    # TODO: Decode the received payload (hint: msg.payload.decode())

    # TODO: Print the topic and the value
    pass


# --- MQTT Client setup ---
# TODO: Instantiate the MQTT client (hint: mqtt.Client)

# TODO: Assign on_connect and on_message callbacks to the client

# TODO: Connect to the broker (hint: client.connect)

# TODO: Start the blocking loop — keeps the subscriber alive (hint: client.loop_forever)