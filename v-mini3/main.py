
"""
Personal Expense & Budget Tracker
Flask Web Application

Run: python main.py
Open: http://127.0.0.1:5000/
"""

from datetime import date, datetime

try:
    from flask import (  # type: ignore[import-not-found]
        Flask,
        render_template,
        request,
        redirect,
        url_for,
        flash,
    )
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "Flask is required to run this app. Install it with: pip install flask"
    ) from exc

from storage import initialize_storage
from expense_manager import (
    add_expense,
    view_expenses,
    edit_expense,
    delete_expense,
    get_spending_summary,
    search_expenses
)
from budget import set_monthly_budget
from utils import validate_date, validate_amount, validate_category


app = Flask(__name__)
app.secret_key = "expense_tracker_local_secret_key"

CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Entertainment",
    "Health",
    "Others"
]


# Initialize JSON files
initialize_storage()


# Dashboard
@app.route("/")
def home():
    try:
        summary = get_spending_summary()
        expenses = view_expenses()

        # Display newest expenses first
        expenses = sorted(
            expenses,
            key=lambda item: item["date"],
            reverse=True
        )

        today = date.today().isoformat()
        current_month = today[:7]

        return render_template(
            "index.html",
            expenses=expenses,
            summary=summary,
            categories=CATEGORIES,
            today=today,
            current_month=current_month
        )

    except Exception as error:
        flash(f"Unable to load dashboard: {error}", "danger")
        return render_template(
            "index.html",
            expenses=[],
            summary={
                "total_today": 0,
                "total_month": 0,
                "category_totals": {},
                "budget": None,
                "remaining_budget": None
            },
            categories=CATEGORIES,
            today=date.today().isoformat(),
            current_month=date.today().strftime("%Y-%m")
        )


# Add expense
@app.route("/add", methods=["POST"])
def add():
    try:
        expense_date = request.form.get("date", "").strip()
        amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()

        validate_date(expense_date)
        amount = validate_amount(amount)
        category = validate_category(category)

        add_expense(
            expense_date,
            amount,
            category,
            description
        )

        flash("Expense added successfully!", "success")

    except ValueError as error:
        flash(str(error), "danger")

    except Exception as error:
        flash(f"Unable to add expense: {error}", "danger")

    return redirect(url_for("home"))


# Edit expense
@app.route("/edit/<expense_id>", methods=["POST"])
def edit(expense_id):
    try:
        expense_date = request.form.get("date", "").strip()
        amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()

        validate_date(expense_date)
        amount = validate_amount(amount)
        category = validate_category(category)

        success = edit_expense(
            expense_id,
            expense_date,
            amount,
            category,
            description
        )

        if success:
            flash("Expense updated successfully!", "success")
        else:
            flash("Expense not found.", "warning")

    except ValueError as error:
        flash(str(error), "danger")

    except Exception as error:
        flash(f"Unable to update expense: {error}", "danger")

    return redirect(url_for("home"))


# Delete expense
@app.route("/delete/<expense_id>", methods=["POST"])
def delete(expense_id):
    try:
        if delete_expense(expense_id):
            flash("Expense deleted successfully!", "success")
        else:
            flash("Expense not found.", "warning")

    except Exception as error:
        flash(f"Unable to delete expense: {error}", "danger")

    return redirect(url_for("home"))


# Set monthly budget
@app.route("/set-budget", methods=["POST"])
def set_budget():
    try:
        month = request.form.get("month", "").strip()
        amount = request.form.get("amount", "").strip()

        # Validate month
        parsed_month = datetime.strptime(month, "%Y-%m")

        if parsed_month.strftime("%Y-%m") != month:
            raise ValueError("Enter month in YYYY-MM format.")

        amount = validate_amount(amount)

        set_monthly_budget(month, amount)

        flash("Monthly budget saved successfully!", "success")

    except ValueError as error:
        flash(str(error), "danger")

    except Exception as error:
        flash(f"Unable to set budget: {error}", "danger")

    return redirect(url_for("home"))


# Search expenses
@app.route("/search")
def search():
    try:
        date_filter = request.args.get("date", "").strip() or None
        category_filter = request.args.get("category", "").strip() or None
        min_amount = request.args.get("min_amount", "").strip()
        max_amount = request.args.get("max_amount", "").strip()

        if date_filter:
            validate_date(date_filter)

        if category_filter:
            category_filter = validate_category(category_filter)

        if min_amount:
            min_amount = validate_amount(min_amount)
        else:
            min_amount = None

        if max_amount:
            max_amount = validate_amount(max_amount)
        else:
            max_amount = None

        if (
            min_amount is not None
            and max_amount is not None
            and max_amount < min_amount
        ):
            raise ValueError("Maximum amount must be greater than minimum amount.")

        expenses = search_expenses(
            date_filter=date_filter,
            category_filter=category_filter,
            min_amount=min_amount,
            max_amount=max_amount
        )

        summary = get_spending_summary()

        return render_template(
            "index.html",
            expenses=expenses,
            summary=summary,
            categories=CATEGORIES,
            today=date.today().isoformat(),
            current_month=date.today().strftime("%Y-%m"),
            search_active=True
        )

    except ValueError as error:
        flash(str(error), "danger")

    except Exception as error:
        flash(f"Search failed: {error}", "danger")

    return redirect(url_for("home"))


# Run Flask application
if __name__ == "__main__":
    app.run(debug=True)
