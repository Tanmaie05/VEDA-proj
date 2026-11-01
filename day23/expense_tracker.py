
import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path(__file__).parent / "expenses.json"


def load_expenses():
    """Load expense records from the JSON file."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict) or not isinstance(
            data.get("expenses"), list
        ):
            raise ValueError("Invalid expense data format.")

        return data["expenses"]

    except FileNotFoundError:
        save_expenses([])
        return []

    except json.JSONDecodeError as exc:
        raise ValueError("expenses.json contains invalid JSON.") from exc


def save_expenses(expenses):
    """Save expense records to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump({"expenses": expenses}, file, indent=4)


def add_expense(date, category, description, amount):
    """Validate and add a new expense."""
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("Enter a valid expense date.") from exc

    category = category.strip()
    description = description.strip()

    if not category:
        raise ValueError("Please select an expense category.")

    if not description:
        raise ValueError("Please enter an expense description.")

    try:
        amount = float(amount)
    except (ValueError, TypeError) as exc:
        raise ValueError("Amount must be a valid number.") from exc

    if amount <= 0:
        raise ValueError("Expense amount must be greater than zero.")

    if not amount < float("inf"):
        raise ValueError("Enter a finite expense amount.")

    expenses = load_expenses()

    expense = {
        "id": max((e.get("id", 0) for e in expenses), default=0) + 1,
        "date": date,
        "category": category,
        "description": description,
        "amount": round(amount, 2)
    }

    expenses.append(expense)
    save_expenses(expenses)

    return expense


def get_summary(expenses):
    """Calculate total and category-wise spending."""
    category_totals = {}

    for expense in expenses:
        category = expense["category"]
        category_totals[category] = (
            category_totals.get(category, 0)
            + float(expense["amount"])
        )

    total = sum(float(e["amount"]) for e in expenses)

    return {
        "total": round(total, 2),
        "count": len(expenses),
        "category_totals": {
            category: round(amount, 2)
            for category, amount in category_totals.items()
        }
    }
