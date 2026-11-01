from flask import Flask, render_template, request

app = Flask(__name__, template_folder=".")


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():

    try:

        # Get numbers from HTML form
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])


        # Perform calculations

        addition = num1 + num2

        subtraction = num1 - num2

        multiplication = num1 * num2


        # Handle division and modulus by zero

        if num2 == 0:

            division = "Cannot divide by zero"

            modulus = "Cannot calculate modulus with zero"

        else:

            division = num1 / num2

            modulus = num1 % num2


        results = {

            "addition": addition,

            "subtraction": subtraction,

            "multiplication": multiplication,

            "division": division,

            "modulus": modulus

        }


        return render_template(
            "index.html",
            results=results
        )


    except ValueError:

        return render_template(
            "index.html",
            error="Please enter valid numbers."
        )


if __name__ == "__main__":

    app.run(debug=True)