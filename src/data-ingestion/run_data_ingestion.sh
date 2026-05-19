#!/bin/bash

# --- Config ---
CONTAINER_NAME="mosquitto_broker"
MQTT_PORT=1883

# --- Start Eclipse Mosquitto Docker ---
echo "Starting Eclipse Mosquitto broker..."
docker run -d \
    --name $CONTAINER_NAME \
    -p 1883:1883 \
    -v "$PWD/src/data-ingestion/mosquitto/log:/mosquitto/log" \
    -v "$PWD/src/data-ingestion/mosquitto/data:/mosquitto/data" \
    eclipse-mosquitto
echo "Waiting for broker to be ready..."
sleep 3

# --- Check broker is running ---
if docker ps | grep -q $CONTAINER_NAME; then
  echo "Broker is up on port $MQTT_PORT"
else
  echo "Failed to start broker. Exiting."
  exit 1
fi

# --- Run publisher ---
echo "Starting publisher..."
python -m src.data-ingestion.pub