# Training

This folder trains the fraud detection model and logs the result to MLflow.

The simple flow is:

```text
data/data.pkl -> preprocessing -> train models -> evaluate -> log to MLflow -> register best model
```

## What Each File Does

| File | Purpose |
| --- | --- |
| `preprocess.py` | Loads the data and prepares it for training |
| `train.py` | Trains the models, evaluates them, and logs results to MLflow |
| `registry.py` | Finds the best model run and registers it if the F1 score is good enough |

## Models Used

The training script compares two models:

- `XGBoost`
- `RandomForest`

Both models are trained on the same train/test split.

## What The Training Script Does

When you run `train.py`, it:

1. loads the dataset from `data/data.pkl`
2. cleans and prepares the data
3. separates features `X` from target `y`
4. splits the data into train and test sets
5. encodes categorical columns with `OneHotEncoder`
6. trains XGBoost and RandomForest
7. evaluates both models
8. logs metrics and artifacts to MLflow
9. registers the best model if it passes the minimum F1 score

## Features And Target

The target column is:

```text
isFraud
```

This is what the model learns to predict.

The other useful columns become features.

Some columns are removed because they can cause leakage or are not useful for prediction:

- `newbalanceOrig`
- `newbalanceDest`
- `isFlaggedFraud`
- `step`

The `step` column is converted into a simpler `time` feature before it is removed.

## Why We Use F1 Score

Fraud detection usually has imbalanced data.

That means most transactions are normal, and only a small number are fraud.

Accuracy alone can be misleading, so this project uses F1 score to compare models.

F1 score balances:

- precision: how many predicted fraud cases were truly fraud
- recall: how many real fraud cases the model caught

The best model is selected using:

```text
f1_score_test
```

## MLflow

MLflow is used to track:

- model runs
- metrics
- trained model artifacts
- confusion matrix images
- registered model versions

The MLflow settings come from `config/config.yml`:

```yaml
mlflow:
  uri: http://127.0.0.1:5123/
  model_name: fraud_detector
  experiment_name: fraud_detection
```

## How To Run

### 1. Start MLflow

From the project root:

```bash
docker compose up mlflow
```

Open MLflow in the browser:

```text
http://127.0.0.1:5123
```

### 2. Run training

In another terminal:

```bash
python3 -m src.training.train
```

## Expected Result

After training, you should see:

- printed training and test scores in the terminal
- two MLflow runs: one for XGBoost and one for RandomForest
- logged metrics such as `accuracy_test` and `f1_score_test`
- confusion matrix images in MLflow artifacts
- a registered model if the best F1 score passes the threshold

## Important Notes

- The registered model is the model that the serving API will load later.
- The minimum F1 threshold is configured in `config/config.yml`.
- Generated MLflow artifacts should not be committed to git.
