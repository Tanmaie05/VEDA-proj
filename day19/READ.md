# Task 19 - Read and Process a Text File

## Objective

The Text File Processing application is a web-based application developed using Python and Flask that allows users to upload a text file and generate useful statistics such as line count, word count, character count, characters excluding spaces, average words per line, and most frequently occurring words.

The project is designed to strengthen understanding of file handling, text processing, regular expressions, collections, exception handling, and Flask-based web development.

## Description

Text files are commonly used for storing notes, documents, reports, logs, and other textual information. Processing these files programmatically makes it possible to quickly analyze their contents and extract useful information.

This application allows users to upload a `.txt` file through a simple web interface. The application reads the uploaded file using Python's file-handling functions and processes its contents to generate different statistics.

The application calculates the total number of lines, words, characters, characters excluding spaces, and average words per line. It also identifies the five most frequently occurring words in the uploaded file.

The project follows a modular structure where text-processing operations are implemented separately, while Flask manages file uploads, user interaction, and dynamic result rendering.

## Technologies Used

• Python 3  
• Flask  
• HTML5  
• CSS3  
• Jinja2 Templates  
• Regular Expressions  
• Python Collections (`Counter`)  
• File Handling  
• VS Code  
• Git & GitHub  

## Features

· Upload and process `.txt` files  
· Automatic line count calculation  
· Automatic word count calculation  
· Character count calculation  
· Character count excluding spaces  
· Average words per line calculation  
· Identification of most frequently used words  
· File type validation  
· Graceful handling of missing or invalid files  
· UTF-8 text file processing  
· Secure filename handling  
· Dynamic statistics display using Flask and Jinja2  
· Modular text-processing structure  
· Clean and responsive web interface  
· Flask-powered localhost web application  
· Fast and automated text analysis  

## Project Structure

```text
day19
│
├── app.py
├── text_processor.py
├── sample.txt
├── README.md
│
├── uploads
│   └── uploaded text files
│
└── templates
    └── index.html