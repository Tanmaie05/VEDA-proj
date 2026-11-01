import json


def load_json(file_path):
    """Load and validate student records from a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError("The JSON file is invalid or incorrectly formatted.") from exc

    if not isinstance(data, dict) or not isinstance(data.get("students"), list):
        raise ValueError("JSON must contain a 'students' list.")

    students = []

    for student in data["students"]:
        if not isinstance(student, dict):
            continue

        if not all(key in student for key in ("id", "name", "department", "marks")):
            continue

        try:
            student_id = int(student["id"])
            name = str(student["name"]).strip()
            department = str(student["department"]).strip()
            marks = float(student["marks"])

            if not name or not department or not 0 <= marks <= 100:
                continue

            students.append({
                "id": student_id,
                "name": name,
                "department": department,
                "marks": marks
            })

        except (ValueError, TypeError):
            continue

    if not students:
        raise ValueError("No valid student records were found.")

    return students


def search_students(students, keyword=""):
    keyword = keyword.strip().lower()

    if not keyword:
        return students

    return [
        student for student in students
        if keyword in student["name"].lower()
        or keyword in student["department"].lower()
        or keyword == str(student["id"])
    ]


def filter_students(students, department="All", minimum_marks=0):
    return [
        student for student in students
        if (department == "All"
            or student["department"].lower() == department.lower())
        and student["marks"] >= minimum_marks
    ]


def generate_summary(students):
    marks = [student["marks"] for student in students]

    return {
        "total_students": len(students),
        "average_marks": sum(marks) / len(marks),
        "highest_marks": max(marks),
        "lowest_marks": min(marks),
        "passed": sum(mark >= 40 for mark in marks),
        "failed": sum(mark < 40 for mark in marks)
    }