"""
P06 - Examination Result Analytics System
Student: Man Patel
Domain: Education

Tkinter desktop application for maintaining examination marks and producing
analytical summaries for faculty use.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

import pandas as pd

from database import load_records, save_records, add_record, update_record, delete_record
from analytics import (
    calculate_student_summary,
    calculate_subject_summary,
    calculate_class_summary,
    get_highest_lowest,
)
from reports import create_subject_report, create_student_report
from validators import validate_record, ValidationError


APP_TITLE = "P06 - Examination Result Analytics System | Man Patel"


class ExaminationApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1250x760")
        self.root.minsize(1050, 650)

        self.df = load_records()
        self.filtered_df = self.df.copy()

        self.vars = {
            "roll_no": tk.StringVar(),
            "student_name": tk.StringVar(),
            "subject": tk.StringVar(),
            "marks": tk.StringVar(),
        }
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")

        self._build_style()
        self._build_header()
        self._build_form()
        self._build_table()
        self._build_footer()
        self.refresh()

    def _build_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("SubTitle.TLabel", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", rowheight=27)
        style.configure("Card.TLabel", font=("Segoe UI", 10, "bold"))

    def _build_header(self):
        frame = ttk.Frame(self.root, padding=(18, 14))
        frame.pack(fill="x")
        ttk.Label(frame, text="Examination Result Analytics System",
                  style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            frame,
            text="Project P06 • Student: Man Patel • Education Domain • Python + Tkinter + Pandas + NumPy + Matplotlib",
            style="SubTitle.TLabel",
        ).pack(anchor="w", pady=(3, 0))

    def _build_form(self):
        outer = ttk.LabelFrame(self.root, text="Student / Subject Marks", padding=10)
        outer.pack(fill="x", padx=18, pady=(0, 10))

        labels = [
            ("Roll No.", "roll_no"),
            ("Student Name", "student_name"),
            ("Subject", "subject"),
            ("Marks (0-100)", "marks"),
        ]

        for col, (label, key) in enumerate(labels):
            ttk.Label(outer, text=label).grid(row=0, column=col * 2, padx=(5, 4), pady=5, sticky="w")
            ttk.Entry(outer, textvariable=self.vars[key], width=22).grid(
                row=0, column=col * 2 + 1, padx=(0, 10), pady=5, sticky="ew"
            )

        for i in range(8):
            outer.columnconfigure(i, weight=1)

        buttons = ttk.Frame(outer)
        buttons.grid(row=1, column=0, columnspan=8, sticky="w", pady=(8, 0))
        ttk.Button(buttons, text="Add Record", command=self.add).pack(side="left", padx=3)
        ttk.Button(buttons, text="Update Selected", command=self.update).pack(side="left", padx=3)
        ttk.Button(buttons, text="Delete Selected", command=self.delete).pack(side="left", padx=3)
        ttk.Button(buttons, text="Clear Form", command=self.clear_form).pack(side="left", padx=3)
        ttk.Button(buttons, text="Import CSV", command=self.import_csv).pack(side="left", padx=3)
        ttk.Button(buttons, text="Export CSV", command=self.export_csv).pack(side="left", padx=3)

    def _build_table(self):
        container = ttk.LabelFrame(self.root, text="Examination Records", padding=8)
        container.pack(fill="both", expand=True, padx=18, pady=(0, 10))

        search = ttk.Frame(container)
        search.pack(fill="x", pady=(0, 8))
        ttk.Label(search, text="Search / Filter:").pack(side="left", padx=(2, 5))
        entry = ttk.Entry(search, textvariable=self.search_var, width=40)
        entry.pack(side="left", padx=5)
        entry.bind("<KeyRelease>", lambda _event: self.refresh())
        ttk.Button(search, text="Show All", command=self.show_all).pack(side="left", padx=5)
        ttk.Button(search, text="Class Summary", command=self.show_class_summary).pack(side="left", padx=5)
        ttk.Button(search, text="Top / Bottom Performers", command=self.show_performers).pack(side="left", padx=5)
        ttk.Button(search, text="Subject Report", command=self.subject_report).pack(side="left", padx=5)
        ttk.Button(search, text="Student Report", command=self.student_report).pack(side="left", padx=5)

        columns = ("roll_no", "student_name", "subject", "marks", "grade")
        self.tree = ttk.Treeview(container, columns=columns, show="headings", selectmode="browse")
        headings = {
            "roll_no": "Roll No.",
            "student_name": "Student Name",
            "subject": "Subject",
            "marks": "Marks",
            "grade": "Grade",
        }
        widths = {"roll_no": 110, "student_name": 250, "subject": 230, "marks": 100, "grade": 100}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")
        self.tree.column("student_name", anchor="w")
        self.tree.column("subject", anchor="w")

        yscroll = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        xscroll = ttk.Scrollbar(container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")
        xscroll.pack(side="bottom", fill="x")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def _build_footer(self):
        footer = ttk.Frame(self.root, padding=(18, 0, 18, 12))
        footer.pack(fill="x")
        self.summary_label = ttk.Label(footer, text="")
        self.summary_label.pack(side="left")
        ttk.Label(footer, textvariable=self.status_var).pack(side="right")

    def _current_record(self):
        return {
            "roll_no": self.vars["roll_no"].get().strip(),
            "student_name": self.vars["student_name"].get().strip(),
            "subject": self.vars["subject"].get().strip(),
            "marks": self.vars["marks"].get().strip(),
        }

    def _handle_error(self, exc):
        if isinstance(exc, ValidationError):
            messagebox.showwarning("Validation", str(exc))
        else:
            messagebox.showerror("Application Error", f"{type(exc).__name__}: {exc}")

    def add(self):
        try:
            record = validate_record(self._current_record())
            self.df = add_record(self.df, record)
            save_records(self.df)
            self.refresh()
            self.clear_form()
            self.status_var.set("Record added successfully.")
        except Exception as exc:
            self._handle_error(exc)

    def update(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Update", "Select a record from the table first.")
            return
        try:
            old = self.tree.item(selected[0], "values")
            old_key = (str(old[0]), str(old[2]))
            record = validate_record(self._current_record())
            self.df = update_record(self.df, old_key, record)
            save_records(self.df)
            self.refresh()
            self.status_var.set("Record updated successfully.")
        except Exception as exc:
            self._handle_error(exc)

    def delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Delete", "Select a record from the table first.")
            return
        values = self.tree.item(selected[0], "values")
        if not messagebox.askyesno("Confirm Delete", f"Delete {values[1]} - {values[2]}?"):
            return
        try:
            key = (str(values[0]), str(values[2]))
            self.df = delete_record(self.df, key)
            save_records(self.df)
            self.refresh()
            self.clear_form()
            self.status_var.set("Record deleted successfully.")
        except Exception as exc:
            self._handle_error(exc)

    def clear_form(self):
        for var in self.vars.values():
            var.set("")
        self.tree.selection_remove(self.tree.selection())

    def on_select(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        self.vars["roll_no"].set(values[0])
        self.vars["student_name"].set(values[1])
        self.vars["subject"].set(values[2])
        self.vars["marks"].set(values[3])

    def refresh(self):
        query = self.search_var.get().strip().lower()
        if query:
            mask = (
                self.df["roll_no"].astype(str).str.lower().str.contains(query, na=False)
                | self.df["student_name"].astype(str).str.lower().str.contains(query, na=False)
                | self.df["subject"].astype(str).str.lower().str.contains(query, na=False)
            )
            self.filtered_df = self.df.loc[mask].copy()
        else:
            self.filtered_df = self.df.copy()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for _, row in self.filtered_df.iterrows():
            marks = float(row["marks"])
            grade = "F" if marks < 40 else ("A+" if marks >= 90 else "A" if marks >= 80 else "B" if marks >= 70 else "C" if marks >= 60 else "D")
            self.tree.insert("", "end", values=(row["roll_no"], row["student_name"], row["subject"], f"{marks:g}", grade))

        students = self.df["roll_no"].nunique() if not self.df.empty else 0
        avg = self.df["marks"].mean() if not self.df.empty else 0
        self.summary_label.config(text=f"Records: {len(self.df)}    Students: {students}    Overall Average: {avg:.2f}")
        self.status_var.set(f"Showing {len(self.filtered_df)} record(s).")

    def show_all(self):
        self.search_var.set("")
        self.refresh()

    def show_class_summary(self):
        try:
            summary = calculate_class_summary(self.df)
            msg = (
                f"Students: {summary['students']}\n"
                f"Subjects: {summary['subjects']}\n"
                f"Records: {summary['records']}\n"
                f"Overall Average: {summary['average']:.2f}\n"
                f"Pass Percentage: {summary['pass_percentage']:.2f}%\n"
                f"Highest Mark: {summary['highest']:.2f}\n"
                f"Lowest Mark: {summary['lowest']:.2f}"
            )
            messagebox.showinfo("Class Performance Summary", msg)
        except Exception as exc:
            self._handle_error(exc)

    def show_performers(self):
        try:
            high, low = get_highest_lowest(self.df)
            if high is None:
                messagebox.showinfo("Performers", "No records available.")
                return
            messagebox.showinfo(
                "Highest / Lowest Performers",
                f"Highest:\n{high['student_name']} ({high['roll_no']}) - {high['average']:.2f}%\n\n"
                f"Lowest:\n{low['student_name']} ({low['roll_no']}) - {low['average']:.2f}%"
            )
        except Exception as exc:
            self._handle_error(exc)

    def subject_report(self):
        try:
            if self.df.empty:
                messagebox.showinfo("Report", "Add some records before creating a report.")
                return
            path = create_subject_report(self.df)
            messagebox.showinfo("Report Created", f"Subject performance report created:\n{path}")
            self.status_var.set("Subject report generated.")
        except Exception as exc:
            self._handle_error(exc)

    def student_report(self):
        try:
            if self.df.empty:
                messagebox.showinfo("Report", "Add some records before creating a report.")
                return
            path = create_student_report(self.df)
            messagebox.showinfo("Report Created", f"Student performance report created:\n{path}")
            self.status_var.set("Student performance report generated.")
        except Exception as exc:
            self._handle_error(exc)

    def import_csv(self):
        path = filedialog.askopenfilename(
            title="Select CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            imported = pd.read_csv(path, dtype=str)
            required = {"roll_no", "student_name", "subject", "marks"}
            if not required.issubset(imported.columns):
                raise ValidationError("CSV must contain: roll_no, student_name, subject, marks")

            cleaned = []
            for _, row in imported.iterrows():
                cleaned.append(validate_record(row.to_dict()))

            new_df = pd.DataFrame(cleaned)
            combined = pd.concat([self.df, new_df], ignore_index=True)
            combined = combined.drop_duplicates(subset=["roll_no", "subject"], keep="last")
            self.df = combined
            save_records(self.df)
            self.refresh()
            messagebox.showinfo("Import", f"Imported {len(new_df)} record(s).")
        except Exception as exc:
            self._handle_error(exc)

    def export_csv(self):
        if self.df.empty:
            messagebox.showinfo("Export", "No records to export.")
            return
        path = filedialog.asksaveasfilename(
            title="Export Records",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return
        try:
            self.df.to_csv(path, index=False)
            messagebox.showinfo("Export", f"Exported records to:\n{path}")
        except Exception as exc:
            self._handle_error(exc)


def main():
    root = tk.Tk()
    ExaminationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
