# Lab 9 - Prefect, Docker, and CI

## Goal

In this lab, you connect the project pieces into a simple operational setup.

This lab covers:

```text
Prefect workflow
Docker Compose services
GitHub Actions image build
GitHub Container Registry
```

## Files To Study

```text
src/orchestration/flows.py
Dockerfile
docker-compose.yml
.github/workflows/ci.yml
```

## Main Ideas

- Prefect runs training and monitoring as workflow tasks.
- Docker Compose runs the local stack.
- Profiles keep one-off jobs separate from always-on services.
- GitHub Actions builds and publishes the project Docker image.

## Run The Main Stack

```bash
docker compose up --build
```

This starts:

```text
mqtt-broker
mlflow
grafana
serving-api
```

## Run One-Off Jobs

Training:

```bash
docker compose --profile jobs run --rm training
```

Monitoring:

```bash
docker compose --profile jobs run --rm monitoring
```

Orchestration:

```bash
docker compose --profile jobs run --rm orchestration
```

## CI Pipeline

The GitHub Actions workflow builds the Docker image and pushes it to:

```text
ghcr.io/<owner>/<repo>
```

## Expected Result

The project can run locally with Docker Compose, and GitHub Actions can publish the project image.
