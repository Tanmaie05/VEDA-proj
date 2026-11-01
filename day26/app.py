
from datetime import date, datetime
from flask import Flask, render_template, request

app = Flask(__name__)


def parse_date(value):
    """Convert YYYY-MM-DD input into a date object."""
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        raise ValueError("Please enter a valid date.")


def calculate_age(dob):
    """Calculate age in completed years."""
    today = date.today()

    if dob > today:
        raise ValueError("Date of birth cannot be in the future.")

    return (
        today.year - dob.year
        - ((today.month, today.day) < (dob.month, dob.day))
    )


def days_between(start_date, end_date):
    """Calculate the absolute number of days between two dates."""
    return abs((end_date - start_date).days)


def calculate_working_days(start_date, end_date):
    """Count weekdays between dates, including both endpoints."""
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    count = 0
    current = start_date

    while current <= end_date:
        if current.weekday() < 5:
            count += 1
        current = date.fromordinal(current.toordinal() + 1)

    return count


def format_date(input_date, format_choice):
    """Format a date using a supported display format."""
    formats = {
        "long": "%B %d, %Y",
        "short": "%d-%m-%Y",
        "iso": "%Y-%m-%d",
        "weekday": "%A, %d %B %Y"
    }

    if format_choice not in formats:
        raise ValueError("Please select a valid date format.")

    return input_date.strftime(formats[format_choice])


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    selected_operation = "age"

    if request.method == "POST":
        selected_operation = request.form.get("operation", "age")

        try:
            if selected_operation == "age":
                dob = parse_date(request.form.get("dob", ""))
                age = calculate_age(dob)
                result = f"Your age is {age} years."

            elif selected_operation == "difference":
                start = parse_date(request.form.get("start_date", ""))
                end = parse_date(request.form.get("end_date", ""))
                total = days_between(start, end)
                result = f"Difference between dates: {total} days."

            elif selected_operation == "working":
                start = parse_date(request.form.get("start_date", ""))
                end = parse_date(request.form.get("end_date", ""))
                total = calculate_working_days(start, end)
                result = (
                    f"Working days: {total} "
                    "(Monday to Friday, including endpoints)."
                )

            elif selected_operation == "format":
                input_date = parse_date(
                    request.form.get("format_date", "")
                )
                choice = request.form.get("format_choice", "")
                result = format_date(input_date, choice)

            elif selected_operation == "current":
                now = datetime.now()
                result = now.strftime("%A, %d %B %Y | %I:%M:%S %p")

            else:
                raise ValueError("Please select a valid operation.")

        except (ValueError, TypeError) as exc:
            error = str(exc)

    return render_template(
        "index.html",
        result=result,
        error=error,
        selected_operation=selected_operation,
        today=date.today().isoformat()
    )


if __name__ == "__main__":
    app.run(debug=True)
