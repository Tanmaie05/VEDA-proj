
from flask import Flask, render_template, request
from utility_module import (
    validate_number,
    format_currency,
    calculate_percentage,
    calculate_total,
    get_file_info
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    file_info = None

    if request.method == "POST":
        action = request.form.get("action")

        try:
            if action == "validate":
                value = request.form.get("value", "").strip()

                if not value:
                    raise ValueError("Please enter a number.")

                result = (
                    f"{value} is a valid number."
                    if validate_number(value)
                    else f"{value} is not a valid number."
                )

            elif action == "currency":
                amount = request.form.get("amount", "").strip()

                if not amount:
                    raise ValueError("Please enter an amount.")

                result = format_currency(amount)

            elif action == "percentage":
                amount = request.form.get("amount", "").strip()
                percentage = request.form.get("percentage", "").strip()

                if not amount or not percentage:
                    raise ValueError("Enter both amount and percentage.")

                value = calculate_percentage(amount, percentage)
                result = f"Calculated percentage: {format_currency(value)}"

            elif action == "total":
                values_text = request.form.get("values", "").strip()

                if not values_text:
                    raise ValueError("Enter numbers separated by commas.")

                values = [v.strip() for v in values_text.split(",")]

                if not all(validate_number(v) for v in values):
                    raise ValueError("Enter only valid finite numbers.")

                result = f"Total: {format_currency(calculate_total(values))}"

            elif action == "file":
                path = request.form.get("file_path", "").strip()

                if not path:
                    raise ValueError("Please enter a file path.")

                file_info = get_file_info(path)

            else:
                raise ValueError("Please select a valid utility.")

        except (ValueError, TypeError, FileNotFoundError, OSError) as exc:
            error = str(exc)

    return render_template(
        "index.html",
        result=result,
        error=error,
        file_info=file_info
    )


if __name__ == "__main__":
    app.run(debug=True)
