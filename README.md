# Projet Structure

```
.
├── config
│   ├── __init__.py
│   ├── config.py
│   ├── config.yml
│   └── readme.txt
├── data
│   ├── data.pkl
│   ├── dataset.csv
│   ├── preprocessed
│   └── ReadMe.txt
├── README.md
├── requirements
│   └── base.txt
├── src
│   ├── dashboard
│   │   └── readme.txt
│   ├── data-ingestion
│   │   ├── __init__.py
│   │   ├── mosquitto
│   │   │   ├── config
│   │   │   ├── data
│   │   │   └── log
│   │   ├── pub.py
│   │   ├── ReadMe.txt
│   │   └── run_data_ingestion.sh
│   ├── monitoring
│   │   └── readme.txt
│   ├── notebooks
│   │   └── create_subset_data.ipynb
│   ├── serving
│   │   └── readme.txt
│   └── training
│       └── readme.txt
└── test
    └── readme.txt

```
## 0. Requirements

| Requirement | Notes |
|-------------|-------|
| **Docker** | Used to run the Eclipse Mosquitto broker |
| **Python 3.8+** | Virtual environment recommended |
| **paho-mqtt** | `pip install paho-mqtt` |
| **pandas** | `pip install pandas` |

---

## 1. Data Ingestion

### Config

You can change the config in `config/config.yml`:

```yml
broker:
  host: 127.0.0.1
  port: 1883
  topic: dsa/transactions
  interval: 30

paths:
  data: data/data.pkl
```

#### Publisher

The publisher reads a fraud detection dataset from a `.pkl` file, and sends one transaction sample to the MQTT broker every 30 seconds.

Each message is a JSON-serialized transaction with a generated UUID:

```json
{
  "type": "PAYMENT",
  "amount": 1716.05,
  "nameOrig": "C913764937",
  "oldbalanceOrg": 5769.17,
  "newbalanceOrig": 4053.13,
  "nameDest": "M1387429131",
  "oldbalanceDest": 0,
  "newbalanceDest": 0,
  "datetime": "2026-05-20 00:57:04",
  "transactionID": "e03e0b58-a31b-44fb-9658-482f1a38c6dd"
}
```
#### Subscriber


### How to run

#### a. Create required folders

From the project root, create the Mosquitto data and log directories:

```bash
mkdir -p src/data-ingestion/mosquitto/data
mkdir -p src/data-ingestion/mosquitto/log
```
---

Samples are sent every **30 seconds**.

#### b. Run

A convenience script handles everything — it starts the Mosquitto broker, then launches the publisher and subscriber automatically.

```bash
chmod +x src/data-ingestion/run_data_ingestion.sh
./src/data-ingestion/run_data_ingestion.sh
```
> The script will:
> 1. Start the Eclipse Mosquitto Docker container
> 2. Wait for the broker to be ready
> 3. Launch the subscriber in the background
> 4. Launch the publisher

---