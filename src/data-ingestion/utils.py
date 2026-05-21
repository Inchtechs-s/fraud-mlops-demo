import os
import sqlite3
from config.config import CONFIG
from datetime import datetime


# --- Config ---
DB_PATH = CONFIG["paths"]["db"]

# -----------------------------------------------------------
# DATABASE
# -----------------------------------------------------------

def init_db():
    """Create DB and table if they don't exist, append otherwise."""
    exists = os.path.exists(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transactionID   TEXT PRIMARY KEY,
            type            TEXT,
            amount          REAL,
            nameOrig        TEXT,
            oldbalanceOrg   REAL,
            newbalanceOrig  REAL,
            diffOrg         REAL, 
            nameDest        TEXT,
            oldbalanceDest  REAL,
            newbalanceDest  REAL,
            diffDest        REAL,
            amountRatio     REAL,
            datetime        TEXT,
            inserted_at     TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()

    if exists:
        count = cursor.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
        print(f"[DB] '{DB_PATH}' already exists — appending ({count} existing rows)")
    else:
        print(f"[DB] '{DB_PATH}' not found — created new database")

    return conn


# -----------------------------------------------------------
# TRANSFORM
# -----------------------------------------------------------

def transform(payload: dict) -> dict:
    """Cast types and compute derived features."""

    # 1. Type casting
    payload["amount"]         = float(payload["amount"])
    payload["oldbalanceOrg"]  = float(payload["oldbalanceOrg"])
    payload["newbalanceOrig"] = float(payload["newbalanceOrig"])
    payload["oldbalanceDest"] = float(payload["oldbalanceDest"])
    payload["newbalanceDest"] = float(payload["newbalanceDest"])

    # 2. Parse datetime
    payload["datetime"] = datetime.strptime(
        payload["datetime"], "%Y-%m-%d %H:%M:%S"
    ).strftime("%Y-%m-%d %H:%M:%S")

    # 3. Derived features
    payload["diffOrg"]     = round(payload["oldbalanceOrg"]  - payload["newbalanceOrig"], 4)
    payload["diffDest"]    = round(payload["newbalanceDest"] - payload["oldbalanceDest"], 4)
    payload["amountRatio"] = (
        round(payload["amount"] / payload["oldbalanceOrg"], 4)
        if payload["oldbalanceOrg"] > 0 else None
    )


    return payload

# -----------------------------------------------------------
# VALIDATE
# -----------------------------------------------------------

def validate(payload: dict) -> bool:
    """Return True if payload is valid, False otherwise."""
    errors = []

    if not payload.get("transactionID"):
        errors.append("Missing transactionID")

    if payload.get("amount", 0) <= 0:
        errors.append(f"Invalid amount: {payload.get('amount')}")

    if not payload.get("nameOrig") or not payload.get("nameDest"):
        errors.append("Missing nameOrig or nameDest")

    if errors:
        print(f"[VALIDATE] Failed — {errors}")
        return False

    return True


# -----------------------------------------------------------
# INSERT
# -----------------------------------------------------------

def insert(conn: sqlite3.Connection, payload: dict):
    """Insert a validated and transformed row into SQLite."""
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO transactions (
                transactionID, type,
                amount, nameOrig, oldbalanceOrg, newbalanceOrig, diffOrg,
                nameDest, oldbalanceDest, newbalanceDest, diffDest,
                 amountRatio, datetime
            ) VALUES (
                :transactionID, :type,
                :amount, :nameOrig, :oldbalanceOrg, :newbalanceOrig, :diffOrg,
                :nameDest, :oldbalanceDest, :newbalanceDest, :diffDest,
                :amountRatio, :datetime
            )
        """, payload)

        conn.commit()
        print(f"[INSERT] Saved transaction {payload['transactionID']}")

    except sqlite3.IntegrityError:
        print(f"[INSERT] Duplicate — skipped {payload['transactionID']}")

    except Exception as e:
        print(f"[INSERT] Error: {e}")

