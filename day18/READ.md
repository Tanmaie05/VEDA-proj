# Task 18 - Practice Exception Handling

## Objective

The Exception Handling Practice application is a web-based application developed using Python and Flask that demonstrates how different runtime exceptions can be safely handled using try, except, else, and finally. The application provides examples of common exceptions such as invalid numeric input, division by zero, missing dictionary keys, invalid list indexes, incompatible data types, and missing files.

The project is designed to strengthen understanding of exception handling, input validation, error management, and Flask-based web development.

## Description

Runtime errors can occur when a program receives invalid input or performs an operation that is not allowed. If these exceptions are not handled properly, they can cause the application to terminate unexpectedly.

This application provides an interactive interface where users can test different types of runtime errors and observe how Python handles them safely.

The application demonstrates ValueError, ZeroDivisionError, KeyError, IndexError, TypeError, and FileNotFoundError. Each exception is handled using a specific except block and a meaningful error message is displayed to the user.

The project follows a modular structure where exception-handling operations are implemented using separate functions, while Flask manages the web interface and user interaction.

## Technologies Used

• Python 3
• Flask
• HTML5
• CSS3
• Jinja2 Templates
• VS Code
• Git & GitHub

## Features

· Demonstrates practical Python exception handling
· Handles invalid numeric input using ValueError
· Handles division by zero using ZeroDivisionError
· Handles missing dictionary keys using KeyError
· Handles invalid list indexes using IndexError
· Handles incompatible data types using TypeError
· Handles missing files using FileNotFoundError
· Uses specific exception handling instead of unnecessary bare except blocks
· Provides meaningful error messages
· Demonstrates try, except, else, and finally
· Interactive testing of different runtime errors
· User-friendly web interface
· Dynamic result rendering using Flask and Jinja2
· Modular code structure using separate exception-handling functions
· Clean and responsive UI design
· Flask-powered localhost web application

## Exception Handling Demonstrations

### ValueError

Occurs when an invalid value is provided where a specific data type is expected.

Example:

```python
float("abc")