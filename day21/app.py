import os

from flask import Flask, render_template, request
from json_processor import (
    load_json,
    search_students,
    filter_students,
    generate_summary
)

app = Flask(__name__)

DATA_FILE = os.path.join(app.root_path, "data.json")


@app.route("/", methods=["GET", "POST"])
def index():
    keyword = ""
    department = "All"
    minimum_marks = 0
    error = None
    students = []
    summary = None

    try:
        all_students = load_json(DATA_FILE)

        if request.method == "POST":
            keyword = request.form.get("keyword", "").strip()
            department = request.form.get("department", "All")

            try:
                minimum_marks = float(
                    request.form.get("minimum_marks", "0")
                )

                if not 0 <= minimum_marks <= 100:
                    raise ValueError

            except ValueError:
                minimum_marks = 0
                error = "Minimum marks must be between 0 and 100."

        filtered = filter_students(
            all_students, department, minimum_marks
        )

        students = search_students(filtered, keyword)
        summary = generate_summary(all_students)

    except (ValueError, OSError) as exc:
        error = str(exc) or "Unable to read the JSON data file."

    return render_template(
        "index.html",
        students=students,
        summary=summary,
        keyword=keyword,
        department=department,
        minimum_marks=minimum_marks,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)