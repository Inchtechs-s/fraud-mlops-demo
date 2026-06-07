FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements/docker.txt requirements/docker.txt
RUN pip install --no-cache-dir -r requirements/docker.txt

COPY . .

CMD ["python", "-m", "src.orchestration.flows"]
