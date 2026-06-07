import os
import sqlite3
from pathlib import Path

import pandas as pd
from evidently import DataDefinition, Dataset, Report
from evidently.presets import DataDriftPreset, DataSummaryPreset

from config.config import CONFIG, ROOT_DIR
from src.training.preprocess import load_data, wrangle


FEATURE_COLUMNS = [
    "type",
    "amount",
    "nameOrig",
    "oldbalanceOrg",
    "nameDest",
    "oldbalanceDest",
    "time",
]
NUMERICAL_COLUMNS = ["amount", "oldbalanceOrg", "oldbalanceDest", "time"]
CATEGORICAL_COLUMNS = ["type", "nameOrig", "nameDest"]
REPORT_PATH = Path(ROOT_DIR) / "reports" / "drift_report.html"


def load_reference_data():
    """Load the training/reference feature set."""
    reference_df = wrangle(load_data())
    reference_df = reference_df.drop(columns=["isFraud"], errors="ignore")
    return reference_df[FEATURE_COLUMNS]


def load_current_data():
    """Load recently ingested transactions from SQLite and align features."""
    table_name = CONFIG["database"]["transactions_table"]
    conn = sqlite3.connect(CONFIG["paths"]["db"])

    try:
        current_df = pd.read_sql_query(
            f"""
            SELECT
                type,
                amount,
                nameOrig,
                oldbalanceOrg,
                nameDest,
                oldbalanceDest,
                datetime
            FROM {table_name}
            """,
            conn,
        )
    finally:
        conn.close()

    if current_df.empty:
        return current_df

    current_df["nameOrig"] = current_df["nameOrig"].str[0]
    current_df["nameDest"] = current_df["nameDest"].str[0]
    current_df["time"] = pd.to_datetime(current_df["datetime"]).dt.hour + 1
    current_df = current_df.drop(columns=["datetime"])

    return current_df[FEATURE_COLUMNS]


def build_drift_report(reference_df, current_df):
    data_definition = DataDefinition(
        numerical_columns=NUMERICAL_COLUMNS,
        categorical_columns=CATEGORICAL_COLUMNS,
    )

    reference = Dataset.from_pandas(reference_df, data_definition=data_definition)
    current = Dataset.from_pandas(current_df, data_definition=data_definition)

    report = Report(
        [
            DataDriftPreset(),
            DataSummaryPreset(),
        ]
    )

    return report.run(current, reference)


def main():
    os.makedirs(REPORT_PATH.parent, exist_ok=True)

    reference_df = load_reference_data()
    current_df = load_current_data()

    if current_df.empty:
        raise ValueError("No ingested transactions found. Run ingestion before drift monitoring.")

    report = build_drift_report(reference_df, current_df)
    report.save_html(str(REPORT_PATH))
    print(f"Saved drift report to {REPORT_PATH}")


if __name__ == "__main__":
    main()
