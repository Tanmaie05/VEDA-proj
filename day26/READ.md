# Day 26 - Date and Time Utility

## Objective

To develop a Python utility application that performs common date and time operations using Python's built-in datetime module.

## Description

The Date and Time Utility is a Flask-based web application that allows users to calculate age, find the difference between dates, count working days, format dates, and view the current date and time.

The application uses reusable Python functions to perform date calculations and validate user input. A simple HTML interface allows users to select an operation and view the result instantly.

## Technologies Used

- Python 3
- Flask
- datetime Module
- HTML5
- CSS3
- Jinja2 Templates

## Features

- Age calculation from date of birth
- Date difference calculation
- Working-day calculation excluding weekends
- Multiple date formatting options
- Current date and time display
- Input validation and error handling
- Interactive Flask web interface

## Project Structure

```text
day26/
├── app.py
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

3. Start the application:

   ```bash
   python app.py
   ```

4. Open `http://127.0.0.1:5000` in your browser.
5. Select a date utility, enter the required information, and view the result.

## Learning Outcomes

- Learned to use Python's datetime module.
- Practiced date parsing and date arithmetic.
- Implemented age and working-day calculations.
- Used functions to organize date-processing logic.
- Practiced input validation and exception handling.
- Integrated Python functionality into a Flask web application.

## Conclusion

This project demonstrates how Python's standard date and time utilities can be used to build a practical web application for accurate date calculations, formatting, and time-related operations.