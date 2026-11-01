import os

from flask import (
    Flask,
    render_template,
    request
)

from werkzeug.utils import secure_filename

from text_processor import process_text


app = Flask(__name__)


# Folder where uploaded files will be stored
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Create uploads folder automatically
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Allowed file types
ALLOWED_EXTENSIONS = {"txt"}


def allowed_file(filename):
    """
    Check whether the uploaded file is a text file.
    """

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


@app.route("/", methods=["GET", "POST"])
def home():

    statistics = None
    error = None
    filename = None

    if request.method == "POST":

        # Get uploaded file
        uploaded_file = request.files.get("file")

        # Check if a file was selected
        if uploaded_file is None:
            error = "Please select a text file."

            return render_template(
                "index.html",
                statistics=statistics,
                error=error,
                filename=filename
            )

        # Check empty filename
        if uploaded_file.filename == "":
            error = "No file selected. Please choose a text file."

            return render_template(
                "index.html",
                statistics=statistics,
                error=error,
                filename=filename
            )

        # Check file extension
        if not allowed_file(uploaded_file.filename):

            error = "Invalid file type. Please upload a .txt file."

            return render_template(
                "index.html",
                statistics=statistics,
                error=error,
                filename=filename
            )

        try:

            filename = secure_filename(
                uploaded_file.filename
            )

            file_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            # Save uploaded file
            uploaded_file.save(file_path)

            # Process text file
            statistics = process_text(file_path)

        except FileNotFoundError:

            error = "The selected file could not be found."

        except PermissionError:

            error = "Permission denied while accessing the file."

        except UnicodeDecodeError:

            error = (
                "Unable to read the file. "
                "Please upload a valid UTF-8 text file."
            )

        except Exception as exception:

            error = (
                f"An unexpected error occurred: "
                f"{exception}"
            )

    return render_template(
        "index.html",
        statistics=statistics,
        error=error,
        filename=filename
    )


if __name__ == "__main__":

    app.run(debug=True)