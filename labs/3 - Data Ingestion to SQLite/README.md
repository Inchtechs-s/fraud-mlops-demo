# Lab 3 - Data Ingestion to SQLite

## Goal

In this lab, you connect MQTT messages to a database.

By the end, a transaction should move through this flow:

```text
publisher -> MQTT broker -> subscriber -> transform -> validate -> SQLite
```

## Files To Study

```text
src/data_ingestion/publisher.py
src/data_ingestion/subscriber.py
src/data_ingestion/utils.py
config/config.yml
```

## Main Ideas

- The publisher reads transaction data and sends one message at a time.
- The MQTT broker receives the message.
- The subscriber listens to the topic.
- The subscriber transforms and validates the payload.
- Valid transactions are inserted into `data/transactions.db`.

## Important Functions

```text
init_db()
transform()
validate()
insert()
```

## Run

Start the broker:

```bash
docker compose up -d mqtt-broker
```

Run the subscriber:

```bash
python -m src.data_ingestion.subscriber
```

Run the publisher in another terminal:

```bash
python -m src.data_ingestion.publisher
```

## Check The Database

```bash
sqlite3 data/transactions.db "SELECT COUNT(*) FROM transactions;"
```

## Expected Result

The number of rows in the `transactions` table should increase as messages are received.
