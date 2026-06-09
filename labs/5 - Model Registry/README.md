# Lab 5 - Model Registry

## Goal

In this lab, you register the best trained model in MLflow.

The registry helps track model versions.

## Files To Study

```text
src/training/registry.py
src/training/train.py
config/config.yml
```

## Main Ideas

- Search MLflow runs.
- Pick the best run using `f1_score_test`.
- Check whether the model passes the minimum score.
- Register the model if it passes.
- Add tags to the registered model version.

## Config

The minimum score is configured here:

```yaml
train:
  min_f1_score: 0.90
```

## Run

```bash
python -m src.training.train
```

Training calls the registry code after logging model runs.

## Expected Result

If the best model passes the threshold, it is added to the MLflow Model Registry.

If it does not pass the threshold, it is skipped.
