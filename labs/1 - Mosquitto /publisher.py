import paho.mqtt.client as mqtt
import time

# --- Config ---
BROKER = ""       # e.g. "test.mosquitto.org"
PORT   = 0       # e.g. 1883
TOPIC  = ""       # must match the publisher topic exactly
INTERVAL = 10


# --- MQTT Client ---

#TODO Instantiate MQTT client and connect to broker (hint: mqtt.Client)

# TODO Connect to broker and start loop (hint: client.connect)

# TODO Start the MQTT client loop to process network events and callbacks (hint: client.loop_start)



# --- Publish loop ---
while True:
    # TODO: Generate a random number between 0 and 100
    value = None
 
    # TODO: Print the value before publishing
    
 
    # TODO: Publish the value to TOPIC (hint: client.publish)
    
 
    time.sleep(INTERVAL)