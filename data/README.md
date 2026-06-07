# Data

## Source

The dataset used in this project comes from the PaySim fraud detection dataset:

https://www.kaggle.com/datasets/ealaxi/paysim1/data

## Current Files

- `data.pkl`: Pickled pandas DataFrame used by the publisher and training notebook.
- `transactions.db`: SQLite database where ingested transactions are stored.

## Data Dictionary

| Column | Description |
| --- | --- |
| `step` | Unit of time in the simulated world. In this dataset, 1 step equals 1 hour. |
| `type` | Transaction type. Possible values are `CASH-IN`, `CASH-OUT`, `DEBIT`, `PAYMENT`, and `TRANSFER`. |
| `amount` | Amount of the transaction in local currency. |
| `nameOrig` | Customer who started the transaction. |
| `oldbalanceOrg` | Sender's initial balance before the transaction. |
| `newbalanceOrig` | Sender's balance after the transaction. |
| `nameDest` | Recipient ID of the transaction. |
| `oldbalanceDest` | Recipient's initial balance before the transaction. |
| `newbalanceDest` | Recipient's balance after the transaction. |
| `isFraud` | Target label. `1` identifies a fraudulent transaction and `0` identifies a non-fraudulent transaction. |
| `isFlaggedFraud` | Rule-based flag for illegal attempts to transfer more than 200,000 in a single transaction. |

## Training vs Inference

For training, `isFraud` is the target label. It should not be used as an input feature.

For live inference, incoming transactions should not include `isFraud`, because the system is trying to predict whether the transaction is fraudulent.

Treat `isFlaggedFraud` carefully. It is a rule-based fraud flag, so using it as a model input can make the model learn an existing rule instead of learning broader fraud behavior.

## Engineered Features

The ingestion pipeline currently enriches transactions with:

| Feature | Meaning |
| --- | --- |
| `diffOrg` | Difference between sender's initial and final balance: `oldbalanceOrg - newbalanceOrig`. |
| `diffDest` | Difference between recipient's final and initial balance: `newbalanceDest - oldbalanceDest`. |
| `amountRatio` | Ratio between transaction amount and sender's initial balance: `amount / oldbalanceOrg`. |
