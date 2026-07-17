# Lab 7 - Grafana Dashboard

## Goal

In this lab, you build a simple Grafana dashboard from the SQLite database.

## Files To Study

```text
docker-compose.yml
data/transactions.db
```

## Main Ideas

- Grafana reads from SQLite using the SQLite datasource plugin.
- The database contains transactions and predictions.
- SQL queries are used to create dashboard panels.

## Run Grafana

```bash
docker compose up -d grafana
```

Open:

```text
http://localhost:3123
```

Default login:

```text
admin / admin
```

## SQLite Datasource Path

Inside the Grafana container, the database is available at:

```text
/project-data/transactions.db
```

## Suggested Panels

```text
Total transactions
Total predictions
High-risk count
High-risk percentage
Risk level breakdown
Latest predictions
Top fraud probabilities
Transaction volume by type
```

## Example Query

```sql
SELECT
  risk_level,
  COUNT(*) AS count
FROM predictions
GROUP BY risk_level;
```

## Expected Result

Grafana should show the current transaction and prediction activity from the database.
