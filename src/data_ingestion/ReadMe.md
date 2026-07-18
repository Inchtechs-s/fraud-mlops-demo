# Data Ingestion

This folder handles the first part of the project: moving transaction data into the database.

The simple flow is:

```text
publisher.py -> MQTT broker -> subscriber.py -> SQLite database
```

## What Each File Does

| File | Purpose |
| --- | --- |
| `publisher.py` | Reads rows from `data/data.pkl` and sends them as MQTT messages |
| `subscriber.py` | Listens for MQTT messages and saves valid transactions |
| `utils.py` | Creates the database table, transforms data, validates data, and inserts rows |
| `run_data_ingestion.sh` | Old helper script. Prefer the manual commands below for now |

## Config Used

The ingestion code reads settings from `config/config.yml`.

Important values:

```yaml
broker:
  host: 127.0.0.1
  port: 1883
  topic: dsa/transactions
  interval: 30

paths:
  data: data/data.pkl
  db: data/transactions.db
```

## How To Run

### 1. Start the MQTT broker

From the project root:

```bash
docker compose up mqtt-broker
```

Leave this running.

### 2. Start the subscriber

Open another terminal:

```bash
python3 -m src.data_ingestion.subscriber
```

The subscriber waits for messages from the MQTT topic.

### 3. Start the publisher

Open a third terminal:

```bash
python3 -m src.data_ingestion.publisher
```

The publisher reads transactions from `data/data.pkl` and sends them to the broker.

## What Happens To Each Transaction

When a transaction arrives, the subscriber:

1. reads the JSON message
2. converts values like amount and balances to numbers
3. creates simple extra fields like `diffOrg`, `diffDest`, and `amountRatio`
4. checks that the message is valid
5. inserts it into the `transactions` table in `data/transactions.db`

## How To Stop

Stop the publisher and subscriber with:

```bash
Ctrl+C
```

Stop the broker with:

```bash
docker compose stop mqtt-broker
```

## Expected Result

After ingestion runs, the SQLite database should contain rows in:

```text
data/transactions.db
```

Table:

```text
transactions
```

This table becomes the stored transaction history used by the rest of the MLOps project.
