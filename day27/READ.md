# Day 27 - Simple API Client

## Objective

To build a Python application that retrieves data from a public REST API, processes JSON responses, and displays selected information in a readable format.

## Description

The Simple API Client is a Flask-based web application that fetches post details from the JSONPlaceholder public REST API using Python's requests library.

Users can enter a post ID to retrieve the corresponding post title, content, user ID, and formatted JSON response. The application includes input validation and error handling for invalid IDs, HTTP errors, connection failures, and request timeouts.

## Technologies Used

- Python 3
- Flask
- Requests
- JSONPlaceholder REST API
- HTML5
- CSS3
- Jinja2 Templates

## Features

- Retrieve data from a public REST API
- Fetch post details using a post ID
- Display formatted JSON responses
- Validate input and post ID ranges
- Handle connection failures and HTTP errors
- Interactive Flask web interface

## Project Structure

```text
day27/
├── app.py
├── README.md
└── templates/
    └── index.html
```

## How to Run

1. Open the project folder in VS Code.
2. Install the required libraries:

   ```bash
   python -m pip install flask requests
   ```

3. Start the application:

   ```bash
   python app.py
   ```

4. Open `http://127.0.0.1:5000` in your browser.
5. Enter a post ID between 1 and 100 and click **Fetch API Data**.

## Learning Outcomes

- Learned the fundamentals of REST APIs.
- Practiced sending HTTP GET requests using Python.
- Understood JSON response handling.
- Implemented HTTP status checks and exception handling.
- Practiced input validation and dynamic HTML rendering.
- Integrated an external API into a Flask application.

## Conclusion

This project demonstrates how Python can interact with external REST APIs to retrieve and display structured information while handling common request errors effectively.