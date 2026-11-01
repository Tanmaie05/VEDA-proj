
from pathlib import Path

from flask import Flask, render_template, request
from file_organizer import organize_files

app = Flask(__name__)

# Restrict organization to the project's test directory.
TEST_FOLDER = Path(app.root_path) / "test_directory"
TEST_FOLDER.mkdir(exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    report = None
    error = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "organize":
            try:
                report = organize_files(TEST_FOLDER)

            except (ValueError, OSError) as exc:
                error = str(exc)

    # Show files currently in the test directory.
    current_files = [
        item.name for item in TEST_FOLDER.iterdir()
        if item.is_file() and not item.is_symlink()
    ]

    return render_template(
        "index.html",
        report=report,
        error=error,
        current_files=current_files
    )


if __name__ == "__main__":
    app.run(debug=True)
