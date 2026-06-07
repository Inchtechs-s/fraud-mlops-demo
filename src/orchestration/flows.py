import subprocess
import sys

from prefect import flow, task


@task
def run_training():
    """Run the existing training pipeline."""
    subprocess.run([sys.executable, "-m", "src.training.train"], check=True)


@task
def run_monitoring():
    """Run the existing Evidently drift report."""
    subprocess.run([sys.executable, "-m", "src.monitoring.drift"], check=True)


@flow(name="fraud-mlops-local-flow")
def mlops_flow(train=True, monitor=True):
    if train:
        run_training()

    if monitor:
        run_monitoring()


if __name__ == "__main__":
    mlops_flow()
