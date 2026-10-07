"""Basic automated tests for P06 modules."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
from analytics import calculate_student_summary, calculate_subject_summary
from validators import validate_record, ValidationError


def test_validation():
    record = validate_record({
        "roll_no": "1", "student_name": "Test Student",
        "subject": "Python", "marks": "80"
    })
    assert record["marks"] == 80.0


def test_invalid_marks():
    try:
        validate_record({
            "roll_no": "1", "student_name": "Test Student",
            "subject": "Python", "marks": "101"
        })
        assert False
    except ValidationError:
        assert True


def test_student_summary():
    df = pd.DataFrame([
        {"roll_no": "1", "student_name": "A", "subject": "P", "marks": 80},
        {"roll_no": "1", "student_name": "A", "subject": "W", "marks": 60},
    ])
    result = calculate_student_summary(df)
    assert float(result.iloc[0]["total"]) == 140
    assert float(result.iloc[0]["average"]) == 70


def test_subject_summary():
    df = pd.DataFrame([
        {"roll_no": "1", "student_name": "A", "subject": "P", "marks": 80},
        {"roll_no": "2", "student_name": "B", "subject": "P", "marks": 60},
    ])
    result = calculate_subject_summary(df)
    assert float(result.iloc[0]["average"]) == 70
