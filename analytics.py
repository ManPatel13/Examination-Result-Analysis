"""Numerical and statistical analysis for P06."""

import numpy as np
import pandas as pd


def grade_from_average(avg):
    """Return a simple academic grade based on average marks."""
    if avg >= 90:
        return "A+"
    if avg >= 80:
        return "A"
    if avg >= 70:
        return "B"
    if avg >= 60:
        return "C"
    if avg >= 40:
        return "D"
    return "F"


def calculate_student_summary(df):
    """Calculate total, average, grade and pass status for every student."""
    if df.empty:
        return pd.DataFrame(columns=["roll_no", "student_name", "total", "average", "grade", "status"])

    grouped = (
        df.groupby(["roll_no", "student_name"], as_index=False)["marks"]
        .agg(total="sum", average="mean", subjects="count")
    )
    grouped["grade"] = grouped["average"].apply(grade_from_average)
    grouped["status"] = np.where(grouped["average"] >= 40, "PASS", "FAIL")
    return grouped.sort_values("average", ascending=False).reset_index(drop=True)


def calculate_subject_summary(df):
    """Calculate subject-wise count, average, highest, lowest and pass percentage."""
    if df.empty:
        return pd.DataFrame(columns=["subject", "count", "average", "highest", "lowest", "pass_percentage"])

    result = (
        df.groupby("subject", as_index=False)["marks"]
        .agg(count="count", average="mean", highest="max", lowest="min")
    )
    passes = df.assign(_pass=df["marks"] >= 40).groupby("subject")["_pass"].mean() * 100
    result["pass_percentage"] = result["subject"].map(passes)
    return result.sort_values("average", ascending=False).reset_index(drop=True)


def calculate_class_summary(df):
    """Return overall class metrics."""
    if df.empty:
        return {
            "students": 0, "subjects": 0, "records": 0, "average": 0.0,
            "pass_percentage": 0.0, "highest": 0.0, "lowest": 0.0
        }
    return {
        "students": int(df["roll_no"].nunique()),
        "subjects": int(df["subject"].nunique()),
        "records": int(len(df)),
        "average": float(np.mean(df["marks"])),
        "pass_percentage": float(np.mean(df["marks"] >= 40) * 100),
        "highest": float(np.max(df["marks"])),
        "lowest": float(np.min(df["marks"])),
    }


def get_highest_lowest(df):
    """Find students with highest and lowest average marks."""
    summary = calculate_student_summary(df)
    if summary.empty:
        return None, None
    return summary.iloc[0].to_dict(), summary.iloc[-1].to_dict()
