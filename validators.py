"""Input validation and custom exceptions for P06."""


class ValidationError(Exception):
    """Raised when user-entered examination data is invalid."""


def validate_record(record):
    """Validate and normalize one examination record."""
    required = ["roll_no", "student_name", "subject", "marks"]
    for key in required:
        if key not in record or str(record[key]).strip() == "":
            raise ValidationError(f"{key.replace('_', ' ').title()} is required.")

    roll_no = str(record["roll_no"]).strip()
    student_name = str(record["student_name"]).strip()
    subject = str(record["subject"]).strip()

    try:
        marks = float(record["marks"])
    except (TypeError, ValueError):
        raise ValidationError("Marks must be a numeric value.")

    if marks < 0 or marks > 100:
        raise ValidationError("Marks must be between 0 and 100.")

    if len(student_name) < 2:
        raise ValidationError("Student name must contain at least 2 characters.")
    if len(subject) < 2:
        raise ValidationError("Subject name must contain at least 2 characters.")

    return {
        "roll_no": roll_no,
        "student_name": student_name,
        "subject": subject,
        "marks": marks,
    }
