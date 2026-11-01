
"""
Expense Manager Module
Handles all expense-related operations.
"""

from datetime import date
from uuid import uuid4

from storage import load_expenses, save_expenses
from utils import validate_date, validate_amount, validate_category


def add_expense(expense_date, amount, category, description):
    """Add a new expense record."""

    validate_date(expense_date)
    amount = validate_amount(amount)
    category = validate_category(category)

    expenses = load_expenses()

    expense = {
        "id": uuid4().hex[:8],
        "date": expense_date,
        "amount": amount,
        "category": category,
        "description": description.strip()
    }

    expenses.append(expense)
    save_expenses(expenses)

    return expense


def view_expenses():
    """Return all expense records."""

    return load_expenses()


def edit_expense(expense_id, expense_date, amount, category, description):
    """Update an existing expense."""

    validate_date(expense_date)
    amount = validate_amount(amount)
    category = validate_category(category)

    expenses = load_expenses()

    for expense in expenses:
        if expense["id"] == expense_id:
            expense["date"] = expense_date
            expense["amount"] = amount
            expense["category"] = category
            expense["description"] = description.strip()

            save_expenses(expenses)
            return True

    return False


def delete_expense(expense_id):
    """Delete an expense using its ID."""

    expenses = load_expenses()

    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            expenses.pop(index)
            save_expenses(expenses)
            return True

    return False


def get_spending_summary():
    """Calculate daily, monthly and category-wise spending."""

    expenses = load_expenses()

    today = date.today().isoformat()
    current_month = today[:7]

    total_today = 0.0
    total_month = 0.0
    category_totals = {}

    for expense in expenses:
        expense_date = expense["date"]
        amount = float(expense["amount"])
        category = expense["category"]

        if expense_date == today:
            total_today += amount

        if expense_date.startswith(current_month):
            total_month += amount

            category_totals[category] = (
                category_totals.get(category, 0.0) + amount
            )

    from budget import get_monthly_budget

    budget_amount = get_monthly_budget(current_month)

    if budget_amount is None:
        remaining_budget = None
    else:
        remaining_budget = budget_amount - total_month

    return {
        "total_today": total_today,
        "total_month": total_month,
        "category_totals": category_totals,
        "budget": budget_amount,
        "remaining_budget": remaining_budget
    }


def search_expenses(
    date_filter=None,
    category_filter=None,
    min_amount=None,
    max_amount=None
):
    """Search expenses using date, category or amount."""

    expenses = load_expenses()
    results = []

    for expense in expenses:

        if date_filter and expense["date"] != date_filter:
            continue

        if (
            category_filter
            and expense["category"].lower() != category_filter.lower()
        ):
            continue

        amount = float(expense["amount"])

        if min_amount is not None and amount < min_amount:
            continue

        if max_amount is not None and amount > max_amount:
            continue

        results.append(expense)

    return results
