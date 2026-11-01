
from pathlib import Path


def validate_number(value):
    """Check whether a value can be converted to a finite number."""
    try:
        number = float(value)
        return number == number and abs(number) != float("inf")
    except (ValueError, TypeError):
        return False


def format_currency(amount):
    """Format a numeric amount to two decimal places."""
    if not validate_number(amount):
        raise ValueError("Amount must be a valid finite number.")

    return f"₹{float(amount):,.2f}"


def calculate_percentage(amount, percentage):
    """Calculate a percentage of an amount."""
    if not validate_number(amount) or not validate_number(percentage):
        raise ValueError("Amount and percentage must be valid numbers.")

    return float(amount) * float(percentage) / 100


def calculate_total(values):
    """Return the sum of a collection of numeric values."""
    if not isinstance(values, (list, tuple)):
        raise TypeError("Values must be a list or tuple.")

    if not all(validate_number(value) for value in values):
        raise ValueError("All values must be valid finite numbers.")

    return sum(float(value) for value in values)


def get_file_info(file_path):
    """Return basic information about an existing file."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not path.is_file():
        raise ValueError("The provided path is not a file.")

    return {
        "name": path.name,
        "extension": path.suffix or "No extension",
        "size_bytes": path.stat().st_size
    }
