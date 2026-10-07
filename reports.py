"""Matplotlib visual reports for P06."""

from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

from analytics import calculate_subject_summary, calculate_student_summary

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"


def _prepare_dir():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)


def create_subject_report(df):
    """Create a subject-wise average/pass-percentage chart."""
    _prepare_dir()
    summary = calculate_subject_summary(df)
    if summary.empty:
        raise ValueError("No subject data is available.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = REPORT_DIR / f"subject_performance_{timestamp}.png"

    x = np.arange(len(summary))
    width = 0.38

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.bar(x - width / 2, summary["average"], width, label="Average Marks")
    ax.bar(x + width / 2, summary["pass_percentage"], width, label="Pass %")
    ax.set_title("Subject-wise Performance Analysis")
    ax.set_xlabel("Subjects")
    ax.set_ylabel("Score / Percentage")
    ax.set_xticks(x)
    ax.set_xticklabels(summary["subject"], rotation=25, ha="right")
    ax.set_ylim(0, 100)
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return str(path)


def create_student_report(df):
    """Create a top-student average performance chart."""
    _prepare_dir()
    summary = calculate_student_summary(df).head(10)
    if summary.empty:
        raise ValueError("No student data is available.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = REPORT_DIR / f"student_performance_{timestamp}.png"

    labels = [f"{r['roll_no']} - {r['student_name']}" for _, r in summary.iterrows()]
    values = summary["average"].to_numpy()

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.barh(labels[::-1], values[::-1])
    ax.set_title("Student Performance Analysis - Top 10")
    ax.set_xlabel("Average Marks (%)")
    ax.set_xlim(0, 100)
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return str(path)
