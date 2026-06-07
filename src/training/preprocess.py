import pandas as pd
from config.config import CONFIG


DATAPATH = CONFIG["paths"]["data"]


def load_data():
    df = pd.read_pickle(DATAPATH)
    return df

def wrangle(df):
    df = df.copy()

    required_columns = {
        "step", "type", "amount", "nameOrig", "oldbalanceOrg",
        "newbalanceOrig", "nameDest", "oldbalanceDest",
        "newbalanceDest", "isFraud", "isFlaggedFraud"
    }

    if required_columns.issubset(df.columns):
        print("All required columns are present.")
    else:
        missing_cols = required_columns - set(df.columns)
        print(f"Warning: Missing columns: {missing_cols}")

    cols = []

    # Features leakage
    cols.append("newbalanceDest")
    cols.append("newbalanceOrig")

    # transform step into time
    df["time"] = df["step"].apply(lambda step: (step - 1) % 24 + 1)
    cols.append("step")

    # System Flag
    cols.append("isFlaggedFraud")

    # keep only type of customers M or C
    df["nameOrig"] = df["nameOrig"].str[0]
    df["nameDest"] = df["nameDest"].str[0]
    

    df.drop(columns=cols, inplace=True, errors="ignore")

    return df
