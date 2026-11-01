
"""
Utility Module
Contains reusable input validation functions.
"""

from datetime import datetime


def validate_amount(amount):
    """Validate that an amount is a positive number."""

    try:
        value = float(amount)

        if value <= 0:
            raise ValueError("Amount must be greater than zero.")

        return round(value, 2)

    except (ValueError, TypeError):
        raise ValueError("Enter a valid positive number.")


def validate_date(date_value):
    """Validate date in YYYY-MM-DD format."""

    try:
        parsed_date = datetime.strptime(date_value, "%Y-%m-%d")

        # Ensure exact format, including leading zeroes.
        if parsed_date.strftime("%Y-%m-%d") != date_value:
            raise ValueError

        return date_value

    except (ValueError, TypeError):
        raise ValueError("Invalid date. Use YYYY-MM-DD format.")


def validate_category(category):
    """Validate that category is not empty."""

    if not isinstance(category, str) or not category.strip():
        raise ValueError("Category cannot be empty.")

    return category.strip().title()


def validate_month(month):
    """Validate month in YYYY-MM format."""

    try:
        parsed_month = datetime.strptime(month, "%Y-%m")

        if parsed_month.strftime("%Y-%m") != month:
            raise ValueError

        return month

    except (ValueError, TypeError):
        raise ValueError("Invalid month. Use YYYY-MM format.")
