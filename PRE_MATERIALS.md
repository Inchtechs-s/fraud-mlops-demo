# Pre-Materials for Students

Welcome to the fraud MLOps bootcamp.

This project shows how a machine learning model can move from a dataset to a small working MLOps system. We will not only train a model. We will also ingest data, track experiments, register a model, serve predictions, monitor behavior, and run the project with Docker.

## What You Should Know Before Class

You do not need to be an expert, but you should be comfortable with:

- basic Python scripts
- pandas DataFrames
- simple machine learning ideas like features, target, train/test split, and model evaluation
- running commands in a terminal
- basic Git and GitHub usage
- basic Docker idea: containers run services in isolated environments

## Tools To Install

Please install these before the session:

| Tool | Why we need it |
| --- | --- |
| Git | To clone and work with the project |
| Python 3.12 or close | To run the Python code |
| Docker Desktop | To run MQTT, MLflow, Grafana, and project containers |
| VS Code or any editor | To read and edit the code |
| A browser | To open MLflow, Grafana, and API docs |

Optional but useful:

- SQLite viewer extension or DB Browser for SQLite
- Postman, Insomnia, or curl for API testing

## Project Setup

Clone the repository:

```bash
git clone <repo-url>
cd fraud-mlops-demo
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the main project dependencies:

```bash
pip install -r requirements/docker.txt
```

Check that Python can see the project:

```bash
python3 -c "import src.training.train; print('Project imports work')"
```

The important thing is that Python can import the project modules.

## Docker Check

Make sure Docker is running, then check:

```bash
docker --version
docker compose version
```

The project uses Docker Compose for services such as:

- MQTT broker
- MLflow
- Grafana
- serving API
- training job
- monitoring job
- orchestration job

## Ports Used In This Project

| Service | URL or Port |
| --- | --- |
| MQTT broker | `1883` |
| MLflow | `http://127.0.0.1:5123` |
| Grafana | `http://127.0.0.1:3123` |
| Serving API | `http://127.0.0.1:8000` |
| FastAPI docs | `http://127.0.0.1:8000/docs` |

If one of these ports is already in use on your machine, tell the instructor before the lab starts.

## Dataset Context

The project uses simulated mobile money transaction data.

Important columns include:

| Column | Meaning |
| --- | --- |
| `step` | Time step. In this dataset, 1 step represents 1 hour |
| `type` | Transaction type, such as `CASH_IN`, `CASH_OUT`, `PAYMENT`, or `TRANSFER` |
| `amount` | Transaction amount |
| `nameOrig` | Customer who started the transaction |
| `oldbalanceOrg` | Sender balance before the transaction |
| `newbalanceOrig` | Sender balance after the transaction |
| `nameDest` | Receiver account |
| `oldbalanceDest` | Receiver balance before the transaction |
| `newbalanceDest` | Receiver balance after the transaction |
| `isFraud` | Target column. `1` means fraud, `0` means not fraud |
| `isFlaggedFraud` | Rule-based fraud flag from the source system |

More details are in [data/README.md](data/README.md).

## Repo Tour

| Folder or file | Purpose |
| --- | --- |
| `config/config.yml` | Main project settings |
| `data/` | Dataset, SQLite databases, and generated local data |
| `src/data_ingestion/` | MQTT publisher, subscriber, validation, and database insert logic |
| `src/training/` | Preprocessing, model training, evaluation, and registry logic |
| `src/serving/` | FastAPI app, model loading, schemas, and prediction code |
| `src/monitoring/` | Evidently monitoring report |
| `src/orchestration/` | Prefect flow |
| `docker-compose.yml` | Local services and jobs |
| `labs/` | Step-by-step bootcamp labs |
| `Visuals.md` | Mermaid diagrams used to explain the system |

## Main Learning Path

During the bootcamp, we will move through these stages:

1. Understand the dataset and the fraud problem
2. Ingest transaction data through MQTT
3. Store transactions in SQLite
4. Train RandomForest and XGBoost models
5. Compare model performance using F1 score
6. Track runs and artifacts with MLflow
7. Register the best model
8. Serve predictions through FastAPI
9. Store prediction results
10. Visualize behavior in Grafana
11. Monitor data drift with Evidently
12. Orchestrate jobs with Prefect
13. Run services with Docker Compose
14. Build and publish Docker images with GitHub Actions

## Commands You Will See

Start core services:

```bash
docker compose up mqtt-broker mlflow grafana serving-api
```

Run data ingestion:

```bash
python3 -m src.data_ingestion.publisher
python3 -m src.data_ingestion.subscriber
```

Usually, the subscriber should be started first in one terminal, then the publisher in another terminal.

Train models:

```bash
python3 -m src.training.train
```

Run monitoring:

```bash
python3 -m src.monitoring.drift
```

Run orchestration:

```bash
python3 -m src.orchestration.flows
```

## What To Review Before The Session

Please read these files before class:

- [README.md](README.md)
- [labs/README.md](labs/README.md)
- [data/README.md](data/README.md)
- [Visuals.md](Visuals.md)

You do not need to memorize the code. Just get familiar with what each part of the project does.

## Simple Concept Checklist

Before the session, try to answer these questions:

- What is the difference between a feature and a target?
- Why do we split data into train and test sets?
- Why is F1 score useful for fraud detection?
- What does MLflow track?
- What does a model registry help us do?
- What is inference?
- Why do we store predictions?
- What is monitoring in MLOps?
- Why do we use Docker Compose?

## Notes For Students

- Do not commit generated artifacts such as MLflow runs, local databases, reports, or cache files.
- Ask questions when a command fails. Most MLOps issues are environment, path, port, or config issues.
- Focus on understanding the flow first. The tools make more sense once the full path is clear.

By the end of the bootcamp, you should be able to explain how a fraud model moves from training to a working local MLOps system.
