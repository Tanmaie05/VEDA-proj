# Task 21 - Create a JSON Data Processor

A Python and Flask web application that reads student information from a JSON file and performs searching, filtering, and summary operations.

## Objective

To learn JSON handling and structured data processing using Python, including reading JSON files, validating records, searching, filtering, and generating statistical summaries.

## Description

JSON (JavaScript Object Notation) is a lightweight data format commonly used to store and exchange structured information. It represents data using key-value pairs, dictionaries, and lists.

This application reads student records from a JSON file and displays them through a Flask-powered web interface. Users can search for students by name, ID, or department, filter records by department, and specify minimum marks.

The application also generates a summary containing the total number of students, average marks, highest marks, lowest marks, and pass/fail counts. Invalid records are skipped during processing to ensure that only valid student information is used.

## Technologies Used

- Python 3
- Flask
- JSON Module
- HTML5
- CSS3
- Jinja2 Templates
- VS Code
- Git & GitHub

## Features

- Read and process structured JSON data
- Search students by name, ID, or department
- Filter student records by department and minimum marks
- Calculate average, highest, and lowest marks
- Display total students and pass/fail statistics
- Validate records and handle invalid JSON data

## Project Structure

```text
day21/
│
├── app.py
├── json_processor.py
├── data.json
├── README.md
│
└── templates/
    └── index.html
```

## Sample JSON Input

The `data.json` file contains student records in the following format:

```json
{
    "students": [
        {
            "id": 101,
            "name": "Aarav",
            "department": "CSE",
            "marks": 85
        },
        {
            "id": 102,
            "name": "Diya",
            "department": "ISE",
            "marks": 92
        }
    ]
}
```

## Installation and Setup

### 1. Open the Project

Open the `day21` folder in VS Code.

### 2. Install Flask

```bash
python -m pip install flask
```

### 3. Run the Application

```bash
python app.py
```

### 4. Open the Application

Open your browser and visit:

```text
http://127.0.0.1:5000
```

### 5. Search and Filter Records

Use the search field to find students by name, ID, or department. Select a department or enter minimum marks to filter the displayed records.

## Expected Output

For the provided six-student dataset, the summary displays:

- Total students: 6
- Average marks: 83.83
- Highest marks: 95
- Lowest marks: 67
- Passed students: 6
- Failed students: 0

The dashboard also displays the matching student records in a formatted table.

## Error Handling

The application handles invalid JSON formatting, missing required fields, invalid student values, and missing or inaccessible data files.

## Learning Outcomes

This project strengthens practical knowledge of JSON file handling, `json.load()`, dictionaries, lists, loops, functions, data validation, searching, filtering, calculations, exception handling, Flask routes, and Jinja2 templates.

## Conclusion

The JSON Data Processor demonstrates how Python can read, validate, search, filter, and summarize structured data. Flask provides a user-friendly interface for interacting with the records and viewing the generated statistics.