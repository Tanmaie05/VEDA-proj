# Student Result & Grade Management System

## Objective

To develop a Python-based application for managing student records, calculating academic results, assigning grades, and summarizing student performance.

## Description

The Student Result & Grade Management System is a Flask web application that allows users to add, search, update, and delete student records. It calculates subject-wise marks, total marks, percentage, grades, and pass/fail status automatically.

Student data is stored in a JSON file, allowing records to persist between application restarts. The dashboard also displays class statistics and identifies the top-performing student.

## Technologies Used

- Python 3
- Flask
- HTML5 and CSS3
- Jinja2
- JSON
- VS Code
- Git and GitHub

## Features

- Add, view, update, and delete student records
- Store student details and subject marks in JSON
- Automatically calculate totals, percentages, grades, and results
- Search students by name or USN
- Display pass/fail counts, class average, and top performer
- Validate marks and prevent duplicate student USNs

## How to Run

1. Install Python 3.
2. Install Flask using `python -m pip install flask`.
3. Run `python app.py`.
4. Open `http://127.0.0.1:5000` in your browser.
5. Add student records and explore the dashboard.

## Project Structure

```text
student-result-management/
├── app.py
├── students.json
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Learning Outcomes

- Practiced Python functions, dictionaries, lists, and validation.
- Implemented CRUD operations and search functionality.
- Learned to store and retrieve structured JSON data.
- Built a responsive web interface using Flask and Jinja2.
- Applied academic grading rules and performance calculations.