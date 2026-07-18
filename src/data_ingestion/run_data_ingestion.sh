#!/bin/bash

# --- Config ---
SERVICE_NAME="mqtt-broker"
CONTAINER_NAME="fraud_mqtt_broker"
MQTT_PORT=1883

# --- Start Eclipse Mosquitto Docker ---
echo "Starting Eclipse Mosquitto broker..."
docker compose up -d $SERVICE_NAME 
echo "Waiting for broker to be ready..."
sleep 3

# --- Check broker is running ---
if docker ps | grep -q $CONTAINER_NAME; then
  echo "Broker is up on port $MQTT_PORT"
else
  echo "Failed to start broker. Exiting."
  exit 1
fi

# --- Run subscriber in background ---
echo "Starting subscriber..."
python -m src.data_ingestion.subscriber & SUB_PID=$!
echo "Subscriber running (PID: $SUB_PID)"

sleep 2  # Give subscriber time to connect before publisher starts


# --- Run publisher ---
echo "Starting publisher..."
python -m src.data_ingestion.publisher