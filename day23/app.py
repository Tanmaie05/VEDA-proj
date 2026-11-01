
from datetime import date, datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from expense_tracker import load_expenses, add_expense, get_summary

app = Flask(__name__)
app.secret_key = "day23-expense-tracker-local-key"


@app.route("/", methods=["GET", "POST"])
def index():
    current_month = date.today().strftime("%Y-%m")

    if request.method == "POST":
        selected_month = request.form.get("selected_month", current_month)

        try:
            add_expense(
                date=request.form.get("date", "").strip(),
                category=request.form.get("category", "").strip(),
                description=request.form.get("description", "").strip(),
                amount=request.form.get("amount", "").strip()
            )
            flash("Expense added successfully!", "success")

        except (ValueError, OSError) as error:
            flash(str(error), "error")

        return redirect(url_for("index", month=selected_month))

    selected_month = request.args.get("month", current_month)

    try:
        all_expenses = load_expenses()

        # Build month options from the dates stored in the JSON file.
        available_months = set()

        for expense in all_expenses:
            expense_date = expense.get("date", "")

            try:
                parsed_date = datetime.strptime(
                    expense_date, "%Y-%m-%d"
                )
                available_months.add(parsed_date.strftime("%Y-%m"))
            except (ValueError, TypeError):
                continue

        # Always include the current month in the dropdown.
        available_months.add(current_month)

        # Keep the requested month if it exists; otherwise use current month.
        if selected_month != "all" and selected_month not in available_months:
            selected_month = current_month

        # Filter records according to the selected month.
        if selected_month == "all":
            filtered_expenses = all_expenses
        else:
            filtered_expenses = [
                expense for expense in all_expenses
                if expense.get("date", "").startswith(selected_month)
            ]

        summary = get_summary(filtered_expenses)
        error = None

    except (ValueError, OSError) as exc:
        all_expenses = []
        filtered_expenses = []
        available_months = {current_month}
        summary = get_summary([])
        error = str(exc)

    months = sorted(available_months, reverse=True)

    # Convert YYYY-MM into a readable month name for the dropdown.
    month_options = []

    for month in months:
        month_date = datetime.strptime(month, "%Y-%m")
        month_options.append({
            "value": month,
            "label": month_date.strftime("%B %Y")
        })

    return render_template(
        "index.html",
        expenses=filtered_expenses,
        summary=summary,
        month_options=month_options,
        selected_month=selected_month,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
