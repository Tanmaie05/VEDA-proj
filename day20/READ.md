# Task 20 - Build a CSV Data Processor

A Python and Flask web application that reads employee data from CSV files and generates a statistical summary report.

## Project Overview

The CSV Data Processor allows users to upload a CSV file containing employee information and automatically calculates useful statistics, including total salary, average salary, highest salary, lowest salary, and total valid employee records.

The application uses Python's built-in CSV module to read and process structured data, validate records, and display the results through a user-friendly web interface.

## Objective

To learn practical CSV file processing using Python and understand file handling, data validation, calculations, lists, dictionaries, loops, functions, and Flask web development.

## Technologies Used

- Python 3
- Flask
- Python CSV Module
- HTML5
- CSS3
- Jinja2 Templates
- VS Code
- Git & GitHub

## Features

- Upload CSV files through a web interface.
- Read employee data using Python's `csv.DictReader()`.
- Validate CSV column headers and employee records.
- Calculate total and average salaries.
- Identify the highest and lowest salaries.
- Count valid employee records.
- Skip invalid records and report the number skipped.
- Display employee details in a formatted table.
- Handle invalid file types and missing data.
- Generate a dynamic summary report.
- Provide a responsive Flask localhost application.

## Project Structure

```text
day20/
│
├── app.py
├── csv_processor.py
├── sample.csv
├── README.md
│
├── uploads/
│
└── templates/
    └── index.html
```

## Sample CSV Dataset

The application uses employee data with the following columns:

```csv
Employee ID,Name,Department,Salary
101,Aarav,IT,45000
102,Diya,HR,38000
103,Rohan,IT,52000
104,Meera,Finance,47000
105,Kiran,Sales,41000
106,Ananya,HR,43000
107,Vikram,Finance,60000
```

Save this dataset as `sample.csv`.

## Sample Output

For the sample dataset, the application generates the following statistics:

| Statistic | Result |
|---|---:|
| Total Employees | 7 |
| Total Salary | 326000.00 |
| Average Salary | 46571.43 |
| Highest Salary | 60000.00 |
| Lowest Salary | 38000.00 |
| Skipped Invalid Records | 0 |

The employee records are also displayed in a table on the webpage.

## Installation and Setup

### 1. Clone or Open the Project

Open the `day20` project folder in VS Code.

### 2. Install Flask

Run the following command in the terminal:

```bash
python -m pip install flask
```

### 3. Start the Application

Run:

```bash
python app.py
```

### 4. Open the Application

Visit the following URL in your browser:

```text
http://127.0.0.1:5000
```

### 5. Process a CSV File

Select a CSV file containing the required employee columns and click **Process CSV File**. The application will display the calculated statistics and employee records.

## Error Handling

The application handles common errors such as:

- No file selected.
- Unsupported file extensions.
- Empty CSV files.
- Missing required columns.
- Missing employee details.
- Invalid or non-numeric salary values.
- Negative salary values.
- File access errors.
- Files exceeding the configured upload size.

Invalid employee rows are skipped, and the report indicates how many records were skipped.

## Learning Outcomes

This project helped develop practical knowledge of:

- CSV file handling using Python.
- Reading structured data with `csv.DictReader()`.
- Data validation and exception handling.
- Lists, dictionaries, and loops.
- Salary calculations using built-in functions.
- Modular programming.
- Flask routes and Jinja2 templates.
- HTML and CSS integration with Python.

## Conclusion

The CSV Data Processor demonstrates how Python can efficiently read, validate, and analyze structured data. Flask provides an accessible web interface for uploading CSV files and viewing the generated statistical report.