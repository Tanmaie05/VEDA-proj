# Personal Information Program

## Description

This project is a simple Personal Information Program developed using Python and Flask.

The program collects basic personal information from the user and displays the information in a formatted profile.

## Information Collected

The program collects:

- Name
- Age
- City
- College
- Course
- Phone Number

## Files

### personal_info.py

This is the original Python console program. It uses:

- Variables
- input()
- print()
- int()
- f-strings

### app.py

This file contains the Flask application and connects the HTML webpage with Python.

### index.html

This file contains the webpage interface and form used to collect personal information.

### README.md

This file contains the project documentation.

## How to Run

### Step 1: Open the project folder

Open the project folder in Visual Studio Code.

### Step 2: Open the terminal

Go to:

Terminal → New Terminal

### Step 3: Create virtual environment

Run:

python -m venv .venv

### Step 4: Activate virtual environment

On Windows PowerShell:

.venv\Scripts\Activate.ps1

### Step 5: Install Flask

Run:

python -m pip install flask

### Step 6: Run the Flask application

Run:

python app.py

### Step 7: Open localhost

Open a web browser and go to:

http://localhost:5000

## Original Python Program

The original console program can be executed using:

python personal_info.py