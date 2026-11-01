import os
import uuid

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from csv_processor import process_csv


app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


@app.route("/", methods=["GET", "POST"])
def index():
    report = None
    error = None
    filename = None

    if request.method == "POST":
        uploaded_file = request.files.get("file")

        if uploaded_file is None or not uploaded_file.filename:
            error = "Please select a CSV file."
        elif not uploaded_file.filename.lower().endswith(".csv"):
            error = "Invalid file type. Please upload a .csv file."
        else:
            safe_name = secure_filename(uploaded_file.filename)

            if not safe_name:
                error = "Invalid filename."
            else:
                # Unique name prevents accidental overwriting.
                saved_name = f"{uuid.uuid4().hex}_{safe_name}"
                file_path = os.path.join(
                    app.config["UPLOAD_FOLDER"], saved_name
                )

                try:
                    uploaded_file.save(file_path)
                    report = process_csv(file_path)
                    filename = safe_name

                except (ValueError, UnicodeDecodeError) as exc:
                    error = str(exc)

                except OSError:
                    error = "The file could not be read or saved."

                finally:
                    if os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                        except OSError:
                            pass

    return render_template(
        "index.html",
        report=report,
        error=error,
        filename=filename
    )


@app.errorhandler(413)
def file_too_large(_error):
    return render_template(
        "index.html",
        report=None,
        error="File is too large. Maximum upload size is 5 MB.",
        filename=None
    ), 413


if __name__ == "__main__":
    app.run(debug=True)