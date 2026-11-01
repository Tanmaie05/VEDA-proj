
import csv
import io
import json
from pathlib import Path

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file,
)

app = Flask(__name__)
app.secret_key = "student-result-project-key"

DATA_FILE = Path(__file__).parent / "students.json"

SUBJECTS = [
    "Python",
    "DBMS",
    "Operating Systems",
    "Computer Networks",
    "Mathematics",
]

MAX_MARKS = 100
PASS_MARK = 35


def load_students():
    """Load student records from the JSON file."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_students(students):
    """Save student records to the JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)


def calculate_result(marks):
    """Calculate total, percentage, grade, and pass/fail status."""
    total = sum(marks.values())
    maximum = len(SUBJECTS) * MAX_MARKS
    percentage = (total / maximum) * 100
    passed = all(marks[subject] >= PASS_MARK for subject in SUBJECTS)

    if not passed:
        grade = "F"
        status = "Fail"
    else:
        status = "Pass"

        if percentage >= 90:
            grade = "O"
        elif percentage >= 80:
            grade = "A+"
        elif percentage >= 70:
            grade = "A"
        elif percentage >= 60:
            grade = "B"
        elif percentage >= 50:
            grade = "C"
        else:
            grade = "D"

    return {
        "total": total,
        "maximum": maximum,
        "percentage": round(percentage, 2),
        "grade": grade,
        "status": status,
    }


def build_student(name, usn, semester, marks, student_id):
    """Build a complete student record."""
    result = calculate_result(marks)

    return {
        "id": student_id,
        "name": name,
        "usn": usn.upper(),
        "semester": semester,
        "marks": marks,
        **result,
    }


def filter_students(students, search_query=""):
    """Filter students by name or USN."""
    query = search_query.strip().lower()

    if not query:
        return students

    return [
        student
        for student in students
        if query in student["name"].lower()
        or query in student["usn"].lower()
    ]


@app.route("/", methods=["GET", "POST"])
def index():
    students = load_students()
    editing_student = None

    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip()
        name = request.form.get("name", "").strip()
        usn = request.form.get("usn", "").strip().upper()
        semester = request.form.get("semester", "").strip()

        if not name or not usn:
            flash("Please enter both the student name and USN.", "error")
            return redirect(url_for("index"))

        if not semester.isdigit() or not 1 <= int(semester) <= 8:
            flash("Semester must be between 1 and 8.", "error")
            return redirect(url_for("index"))

        marks = {}

        try:
            for subject in SUBJECTS:
                value = request.form.get(subject, "").strip()

                if not value:
                    raise ValueError(f"Enter marks for {subject}.")

                mark = float(value)

                if not mark.is_integer() or not 0 <= mark <= MAX_MARKS:
                    raise ValueError(
                        f"{subject} marks must be a whole number from 0 to 100."
                    )

                marks[subject] = int(mark)

        except ValueError as exc:
            flash(str(exc), "error")
            return redirect(url_for("index"))

        duplicate = any(
            student["usn"].upper() == usn
            and str(student["id"]) != student_id
            for student in students
        )

        if duplicate:
            flash("A student with this USN already exists.", "error")
            return redirect(url_for("index"))

        if student_id:
            existing = next(
                (s for s in students if str(s["id"]) == student_id),
                None,
            )

            if existing:
                updated = build_student(
                    name, usn, int(semester), marks, existing["id"]
                )
                students = [
                    updated if str(s["id"]) == student_id else s
                    for s in students
                ]
                flash("Student record updated successfully.", "success")
            else:
                flash("Student record was not found.", "error")
        else:
            new_id = max(
                (int(s.get("id", 0)) for s in students),
                default=0,
            ) + 1

            students.append(
                build_student(name, usn, int(semester), marks, new_id)
            )
            flash("Student added successfully.", "success")

        save_students(students)
        return redirect(url_for("index"))

    edit_id = request.args.get("edit", "").strip()

    if edit_id:
        editing_student = next(
            (s for s in students if str(s["id"]) == edit_id),
            None,
        )

    search_query = request.args.get("search", "").strip()
    filtered_students = filter_students(students, search_query)

    total_students = len(students)
    passed_students = sum(s["status"] == "Pass" for s in students)
    failed_students = total_students - passed_students

    average_percentage = (
        round(sum(s["percentage"] for s in students) / total_students, 2)
        if total_students
        else 0
    )

    top_student = max(
        students,
        key=lambda s: s["percentage"],
        default=None,
    )

    return render_template(
        "index.html",
        subjects=SUBJECTS,
        students=filtered_students,
        editing_student=editing_student,
        search_query=search_query,
        total_students=total_students,
        passed_students=passed_students,
        failed_students=failed_students,
        average_percentage=average_percentage,
        top_student=top_student,
    )


@app.route("/export")
def export_results():
    """Download all student results or only search-matched records."""
    search_query = request.args.get("search", "").strip()
    students = filter_students(load_students(), search_query)

    output = io.StringIO(newline="")
    writer = csv.writer(output)

    headers = [
        "Student ID",
        "Student Name",
        "USN",
        "Semester",
        *SUBJECTS,
        "Total Marks",
        "Maximum Marks",
        "Percentage",
        "Grade",
        "Result",
    ]
    writer.writerow(headers)

    for student in students:
        marks = student.get("marks", {})

        writer.writerow([
            student.get("id", ""),
            student.get("name", ""),
            student.get("usn", ""),
            student.get("semester", ""),
            *[marks.get(subject, "") for subject in SUBJECTS],
            student.get("total", ""),
            student.get("maximum", ""),
            student.get("percentage", ""),
            student.get("grade", ""),
            student.get("status", ""),
        ])

    csv_bytes = io.BytesIO(output.getvalue().encode("utf-8-sig"))
    output.close()

    filename = (
        "student_search_results.csv"
        if search_query
        else "student_results.csv"
    )

    return send_file(
        csv_bytes,
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename,
    )


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    students = load_students()

    updated_students = [
        student
        for student in students
        if int(student["id"]) != student_id
    ]

    if len(updated_students) == len(students):
        flash("Student record was not found.", "error")
    else:
        save_students(updated_students)
        flash("Student record deleted successfully.", "success")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
