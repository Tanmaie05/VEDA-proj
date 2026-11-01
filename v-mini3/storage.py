
"""
Storage Module
Handles JSON file creation, reading and writing.
"""

import json
import os


EXPENSE_FILE = "expenses.json"
BUDGET_FILE = "budgets.json"


def initialize_storage():
    """Create JSON files if they do not exist."""

    if not os.path.exists(EXPENSE_FILE):
        save_json(EXPENSE_FILE, [])

    if not os.path.exists(BUDGET_FILE):
        save_json(BUDGET_FILE, {})


def load_json(filename, default_data):
    """Load JSON data safely."""

    if not os.path.exists(filename):
        save_json(filename, default_data)
        return default_data.copy()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, type(default_data)):
            return data

        raise ValueError(f"Invalid data structure in {filename}")

    except json.JSONDecodeError:
        print(f"Warning: {filename} contains invalid JSON.")
        print("Starting with empty data for this file.")
        return default_data.copy()

    except (OSError, ValueError) as error:
        print(f"Storage error in {filename}: {error}")
        return default_data.copy()


def save_json(filename, data):
    """Save data to a JSON file."""

    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    except (OSError, TypeError) as error:
        raise RuntimeError(
            f"Could not save {filename}: {error}"
        ) from error


def load_expenses():
    """Load all expenses."""

    data = load_json(EXPENSE_FILE, [])

    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Invalid expense records in expenses.json")

    return data


def save_expenses(expenses):
    """Save all expenses."""

    save_json(EXPENSE_FILE, expenses)


def load_budgets():
    """Load all monthly budgets."""

    return load_json(BUDGET_FILE, {})


def save_budgets(budgets):
    """Save all monthly budgets."""

    save_json(BUDGET_FILE, budgets)
