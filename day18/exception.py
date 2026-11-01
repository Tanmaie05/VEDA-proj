# TASK 18 - PRACTICE EXCEPTION HANDLING


def handle_numeric_input(value):
    """
    Demonstrates ValueError handling
    when converting user input into a number.
    """

    try:
        number = float(value)

    except ValueError:
        return {
            "success": False,
            "message": "Invalid numeric input. Please enter a valid number."
        }

    else:
        return {
            "success": True,
            "message": f"Valid number entered: {number}"
        }

    finally:
        pass


def handle_division(first_value, second_value):
    """
    Demonstrates ZeroDivisionError handling.
    """

    try:
        first = float(first_value)
        second = float(second_value)

        result = first / second

    except ValueError:
        return {
            "success": False,
            "message": "Both values must be valid numbers."
        }

    except ZeroDivisionError:
        return {
            "success": False,
            "message": "Division by zero is not allowed."
        }

    else:
        return {
            "success": True,
            "message": f"Division result: {result:.2f}"
        }

    finally:
        pass


def handle_missing_key(key):
    """
    Demonstrates KeyError handling
    using a dictionary.
    """

    employee = {
        "name": "Tanmaie",
        "department": "Computer Science",
        "role": "Python Intern"
    }

    try:
        value = employee[key]

    except KeyError:
        return {
            "success": False,
            "message": f"KeyError: '{key}' does not exist in the employee record."
        }

    else:
        return {
            "success": True,
            "message": f"Value found: {value}"
        }

    finally:
        pass


def handle_list_index(index):
    """
    Demonstrates IndexError handling
    using a list.
    """

    subjects = [
        "Python",
        "Flask",
        "SQL"
    ]

    try:
        position = int(index)

        subject = subjects[position]

    except ValueError:
        return {
            "success": False,
            "message": "List index must be an integer."
        }

    except IndexError:
        return {
            "success": False,
            "message": "IndexError: The requested list position does not exist."
        }

    else:
        return {
            "success": True,
            "message": f"Subject found: {subject}"
        }

    finally:
        pass


def handle_type_error():
    """
    Demonstrates TypeError handling.
    """

    try:
        number = 100
        text = "Python"

        result = number + text

    except TypeError:
        return {
            "success": False,
            "message": "TypeError: Incompatible data types cannot be combined."
        }

    else:
        return {
            "success": True,
            "message": f"Result: {result}"
        }

    finally:
        pass


def handle_file_error(filename):
    """
    Demonstrates FileNotFoundError handling.
    """

    try:
        with open(filename, "r") as file:
            content = file.read()

    except FileNotFoundError:
        return {
            "success": False,
            "message": f"FileNotFoundError: '{filename}' was not found."
        }

    except PermissionError:
        return {
            "success": False,
            "message": "Permission denied while accessing the file."
        }

    else:
        return {
            "success": True,
            "message": "File read successfully."
        }

    finally:
        pass