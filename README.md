# P06 - Examination Result Analytics System

**Student:** Man Patel  
**Project No.:** P06  
**Domain:** Education  
**Technology:** Python, Tkinter, Pandas, NumPy, Matplotlib, CSV file handling

## 1. Problem Statement
A department needs to maintain examination results and quickly understand class
performance, subject-wise results, and students whose results require attention.

## 2. Objective
Develop an application for maintaining examination results and producing
analytical summaries for faculty use.

## 3. Functional Requirements Covered
- Maintain student and subject marks.
- Add, view, search/filter, update and delete records.
- Calculate totals, averages and grades.
- Identify highest and lowest performers.
- Produce class and subject-wise summaries.
- Generate at least two meaningful visual reports.
- Import/export CSV data.
- Validate input and handle exceptions.

## 4. Technical Requirements Covered
- Python functions and data structures.
- Persistent file handling using CSV.
- More than three user-defined modules:
  `main.py`, `database.py`, `analytics.py`, `reports.py`, `validators.py`.
- Pandas and NumPy for data processing.
- Tkinter GUI.
- Matplotlib visualizations.
- Input validation and exception handling.
- Documentation and automated tests.

## 5. Project Structure
```text
Man_Patel_P06_Examination_Result_Analytics/
│
├── main.py
├── database.py
├── analytics.py
├── reports.py
├── validators.py
├── requirements.txt
├── README.md
├── sample_data.csv
├── data/
│   └── exam_results.csv
├── reports/
└── tests/
    └── test_app.py
```

## 6. Installation
Open a terminal in this folder:

```bash
python -m pip install -r requirements.txt
```

Tkinter normally comes with Python on Windows. If it is missing, install the
Tk/Tcl component of your Python distribution.

## 7. Run
```bash
python main.py
```

The application opens as a desktop GUI.

## 8. How to Use
1. Enter Roll No., Student Name, Subject and Marks.
2. Click **Add Record**.
3. Select a table row to edit it and use **Update Selected**.
4. Use **Delete Selected** to remove a record.
5. Use the search box to filter by roll number, student or subject.
6. Click **Class Summary** for overall statistics.
7. Click **Top / Bottom Performers** to identify students needing attention.
8. Click **Subject Report** to create a subject-wise Matplotlib chart.
9. Click **Student Report** to create a student-performance chart.
10. Use Import/Export CSV for data transfer.

## 9. Grade Logic
| Average | Grade |
|---|---|
| 90-100 | A+ |
| 80-89.99 | A |
| 70-79.99 | B |
| 60-69.99 | C |
| 40-59.99 | D |
| Below 40 | F |

## 10. Testing
From the project folder:

```bash
python -m pytest tests
```

The tests cover validation and basic student/subject analysis.

## 11. Suggested Viva Explanation
This project solves the problem of maintaining examination results and converting
raw marks into useful faculty information. CSV provides persistent storage,
Pandas manages tabular data, NumPy performs numerical calculations, Tkinter
provides the desktop interface, and Matplotlib creates visual reports.
