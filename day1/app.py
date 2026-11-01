from flask import Flask, render_template, request
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=BASE_DIR)


@app.route("/", methods=["GET", "POST"])
def home():
    profile = None

    if request.method == "POST":
        profile = {
            "name": request.form.get("name", ""),
            "age": request.form.get("age", ""),
            "city": request.form.get("city", ""),
            "college": request.form.get("college", ""),
            "course": request.form.get("course", ""),
            "phone": request.form.get("phone", "")
        }

    return render_template(
        "index.html",
        profile=profile
    )


if __name__ == "__main__":
    app.run(debug=True)