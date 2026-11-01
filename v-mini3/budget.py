
"""
Budget Module
Handles monthly budget operations.
"""

from datetime import datetime

from storage import load_budgets, save_budgets
from utils import validate_amount


def validate_month(month):
    """Validate month format YYYY-MM."""

    try:
        datetime.strptime(month, "%Y-%m")
        return month

    except ValueError:
        raise ValueError("Month must be in YYYY-MM format.")


def set_monthly_budget(month, amount):
    """Set or update a monthly budget."""

    validate_month(month)
    amount = validate_amount(amount)

    budgets = load_budgets()

    budgets[month] = amount

    save_budgets(budgets)

    return True


def get_monthly_budget(month):
    """Get the budget for a particular month."""

    validate_month(month)

    budgets = load_budgets()

    amount = budgets.get(month)

    if amount is None:
        return None

    return float(amount)


def view_all_budgets():
    """Return all saved monthly budgets."""

    return load_budgets()
