"""Persistent CSV storage and CRUD operations for P06."""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "exam_results.csv"
COLUMNS = ["roll_no", "student_name", "subject", "marks"]


def _ensure_storage():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        pd.DataFrame(columns=COLUMNS).to_csv(DATA_FILE, index=False)


def load_records():
    """Load examination records from the CSV file."""
    try:
        _ensure_storage()
        df = pd.read_csv(DATA_FILE, dtype={"roll_no": str, "student_name": str, "subject": str})
        if df.empty:
            return pd.DataFrame(columns=COLUMNS)
        df["marks"] = pd.to_numeric(df["marks"], errors="coerce")
        df = df.dropna(subset=["marks"]).copy()
        df["marks"] = df["marks"].astype(float)
        return df[COLUMNS]
    except (OSError, pd.errors.ParserError, ValueError):
        return pd.DataFrame(columns=COLUMNS)


def save_records(df):
    """Persist the complete DataFrame to CSV."""
    _ensure_storage()
    out = df[COLUMNS].copy()
    out.to_csv(DATA_FILE, index=False)


def add_record(df, record):
    """Add a unique roll-number/subject record."""
    key_exists = (
        (df["roll_no"].astype(str) == str(record["roll_no"]))
        & (df["subject"].str.lower() == record["subject"].lower())
    ).any()
    if key_exists:
        raise ValueError("A record for this roll number and subject already exists.")
    return pd.concat([df, pd.DataFrame([record])], ignore_index=True)


def update_record(df, old_key, record):
    """Update the selected record identified by (roll_no, subject)."""
    roll_no, subject = old_key
    mask = (df["roll_no"].astype(str) == str(roll_no)) & (df["subject"].str.lower() == subject.lower())
    if not mask.any():
        raise ValueError("Selected record was not found.")
    duplicate = (
        (df["roll_no"].astype(str) == str(record["roll_no"]))
        & (df["subject"].str.lower() == record["subject"].lower())
    )
    duplicate_count = int(duplicate.sum())
    if duplicate_count > 1 or (duplicate_count == 1 and not bool(mask[duplicate].iloc[0])):
        raise ValueError("The updated roll number/subject would duplicate another record.")

    for col in ["roll_no", "student_name", "subject", "marks"]:
        df.loc[mask, col] = record[col]
    df["marks"] = pd.to_numeric(df["marks"])
    return df


def delete_record(df, key):
    """Delete one roll-number/subject record."""
    roll_no, subject = key
    mask = (df["roll_no"].astype(str) == str(roll_no)) & (df["subject"].str.lower() == subject.lower())
    if not mask.any():
        raise ValueError("Selected record was not found.")
    return df.loc[~mask].reset_index(drop=True)
