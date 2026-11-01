from flask import Flask, render_template, request

app = Flask(__name__, template_folder=".")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check_number():

    try:

        number = int(request.form["number"])

        if number % 2 == 0:
            result = f"{number} is an EVEN number."
            result_type = "even"
        else:
            result = f"{number} is an ODD number."
            result_type = "odd"

        return render_template(
            "index.html",
            result=result,
            result_type=result_type,
            number=number
        )

    except ValueError:

        return render_template(
            "index.html",
            error="Please enter a valid integer."
        )


if __name__ == "__main__":
    app.run(debug=True)