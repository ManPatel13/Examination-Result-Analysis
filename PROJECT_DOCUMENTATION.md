# Project Documentation - P06

## Student Details
- **Name:** Man Patel
- **Project No.:** P06
- **Domain:** Education
- **Project Title:** Examination Result Analytics System

## Abstract
The Examination Result Analytics System is a Python-based desktop application
designed for departments and faculty members to maintain examination marks and
quickly understand class performance. The application stores student and
subject marks in a persistent CSV file, supports CRUD operations, calculates
totals, averages and grades, identifies high/low performers, and creates
visual analytical reports.

## Modules
### 1. main.py
Provides the Tkinter graphical user interface and connects all application
features.

### 2. database.py
Handles persistent CSV storage and CRUD operations.

### 3. analytics.py
Uses Pandas and NumPy to calculate student summaries, subject summaries,
class statistics, grades and highest/lowest performers.

### 4. reports.py
Uses Matplotlib to generate two visual reports:
- Subject-wise average and pass percentage.
- Top student average performance.

### 5. validators.py
Provides input validation and a custom `ValidationError` exception.

## Data Flow
```text
User Input
   ↓
Tkinter GUI
   ↓
Validation
   ↓
CSV Storage
   ↓
Pandas / NumPy Analysis
   ↓
Class + Student + Subject Summaries
   ↓
Matplotlib Visual Reports
```

## Error Handling
The application catches invalid marks, missing fields, duplicate records,
missing selections, malformed CSV files and file-system errors. User-friendly
messages are shown with Tkinter message boxes.

## Future Scope
- Login system for faculty/admin.
- SQLite/MySQL database.
- PDF report generation.
- Attendance + examination integration.
- Student login and result portal.
- More advanced analytics such as semester trends.
