# Lab 8 - Evidently Monitoring

## Goal

In this lab, you generate a simple data drift report.

The report compares:

```text
reference data = training data
current data = ingested transactions
```

## Files To Study

```text
src/monitoring/drift.py
requirements/monitoring.txt
```

## Main Ideas

- Reference data comes from the original training dataset.
- Current data comes from `data/transactions.db`.
- Evidently compares feature distributions.
- The output is an HTML report.

## Run

Install requirements:

```bash
pip install -r requirements/monitoring.txt
```

Generate report:

```bash
python -m src.monitoring.drift
```

## Output

```text
reports/drift_report.html
```

## Expected Result

Open the HTML report and review whether current transaction data differs from reference training data.
