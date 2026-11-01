# Day 30 – Log File Analyzer

## Objective

To develop a Python application that analyzes server log files and generates useful statistics about requests, errors, IP addresses, and endpoints.

## Description

The Log File Analyzer is a Flask-based web application that processes server access logs and presents the results in an organized dashboard. Users can upload `.log` or `.txt` files or test the application using sample data.

The application extracts information from valid log entries, calculates request statistics, identifies frequent IP addresses and endpoints, and reports malformed lines that could not be processed.

## Technologies Used

- Python 3
- Flask
- HTML5 and CSS3
- Jinja2
- Regular Expressions
- Collections Counter

## Features

- Server log file upload and processing
- Request and error response statistics
- Top IP address and endpoint analysis
- HTTP status code and method summaries
- Invalid log line handling and file validation
- Responsive localhost dashboard

## How to Run

1. Open the project folder in VS Code.
2. Activate your virtual environment, if you use one.
3. Install Flask:

   ```bash
   python -m pip install flask
   ```

4. Run the application:

   ```bash
   python app.py
   ```

5. Open `http://127.0.0.1:5000` in your browser.
6. Upload a server log file or click **Try Sample Log Data**.

## Project Structure

```text
day30/
├── app.py
├── README.md
└── templates/
    └── index.html
```

## Learning Outcomes

- Practiced Python string processing and regular expressions.
- Used dictionaries and `Counter` to analyze data.
- Learned to process files and handle malformed records.
- Built a web interface using Flask and Jinja2.
- Practiced input validation and error handling.

## Note

The application supports a common Apache/Nginx access-log format. Logs in other formats may require changes to the parsing pattern.