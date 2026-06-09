# Lab 4 - Training Pipeline

## Goal

In this lab, you move from notebook-style training to a repeatable Python training pipeline.

By the end, this command should train models and log results:

```bash
python -m src.training.train
```

## Files To Study

```text
src/training/preprocess.py
src/training/train.py
config/config.yml
```

## Main Ideas

- Load the training data.
- Clean and prepare the data.
- Split features and target.
- Train models.
- Evaluate the models.
- Log metrics and artifacts to MLflow.

## Feature And Target Split

The model uses:

```text
X = input features
y = isFraud
```

`isFraud` is the target column because it is what the model is trying to predict.

## Models Used

```text
XGBoost
Random Forest
```

## Metrics

Focus on:

```text
accuracy
f1_score
confusion matrix
```

For fraud detection, `f1_score` is more useful than accuracy alone.

## Run

Start MLflow:

```bash
docker compose up -d mlflow
```

Run training:

```bash
python -m src.training.train
```

## Expected Result

MLflow should contain training runs with metrics, model artifacts, and confusion matrix figures.
