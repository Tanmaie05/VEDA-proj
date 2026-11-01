from flask import Flask, render_template, request

from salary import calculate_salary


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    employee_name = ""
    employee_id = ""
    salary = None
    error = None

    if request.method == "POST":

        employee_name = request.form.get(
            "employee_name",
            ""
        ).strip()

        employee_id = request.form.get(
            "employee_id",
            ""
        ).strip()

        basic_salary_input = request.form.get(
            "basic_salary",
            ""
        ).strip()

        if not employee_name:

            error = "Employee name cannot be empty."

        elif not employee_id:

            error = "Employee ID cannot be empty."

        elif not basic_salary_input:

            error = "Please enter basic salary."

        else:

            try:

                basic_salary = float(
                    basic_salary_input
                )

                if basic_salary <= 0:

                    error = (
                        "Basic salary must be "
                        "greater than zero."
                    )

                else:

                    salary = calculate_salary(
                        basic_salary
                    )

            except ValueError:

                error = (
                    "Invalid salary! "
                    "Please enter a valid number."
                )

    return render_template(
        "index.html",
        employee_name=employee_name,
        employee_id=employee_id,
        salary=salary,
        error=error
    )


if __name__ == "__main__":

    app.run(debug=True)