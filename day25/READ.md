# Day 25 - Python Utility Module

## Objective

To develop a reusable Python utility module containing commonly needed functions for validation, formatting, calculations, and file operations.

## Description

The Python Utility Module demonstrates modular programming by organizing reusable functions in a separate Python file. The application provides utilities for validating numbers, formatting currency, calculating percentages, calculating totals, and retrieving file information.

A Flask-based web interface allows users to test these functions and view their results. The project emphasizes code reusability, input validation, exception handling, and maintainable programming practices.

## Technologies Used

- Python 3
- Flask
- HTML5
- CSS3
- Jinja2 Templates
- pathlib

## Features

- Reusable utility functions in a separate Python module
- Numeric validation and error handling
- Currency formatting with two decimal places
- Percentage and total calculations
- File information retrieval
- Interactive Flask web interface

## Project Structure

```text
day25/
├── app.py
├── utility_module.py
├── README.md
└── templates/
    └── index.html
```

## How to Run

1. Open the project folder in VS Code.
2. Install Flask:

   ```bash
   python -m pip install flask
   ```

3. Run the application:

   ```bash
   python app.py
   ```

4. Open `http://127.0.0.1:5000` in your browser.
5. Select a utility, enter the required input, and view the result.

## Learning Outcomes

- Learned how to create and import custom Python modules.
- Practiced writing reusable functions with clear responsibilities.
- Implemented numeric validation and exception handling.
- Worked with currency formatting and mathematical calculations.
- Used Python's pathlib module to retrieve file information.
- Integrated reusable Python functions into a Flask application.

## Conclusion

This project demonstrates how modular programming helps organize reusable functionality and makes Python applications easier to maintain, test, and extend.
