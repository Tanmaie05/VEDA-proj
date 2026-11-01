# Task 22 - Build a File Organizer

A Python script that automatically organizes files into folders based on their file extensions.

## Objective

To learn filesystem automation using Python and understand how to scan directories, identify file types, move files, and organize folders efficiently.

## Description

Files are often stored in a single directory, making it difficult to locate specific documents, images, and other resources. Manually organizing these files can be time-consuming.

The File Organizer automates this process by scanning a specified directory and moving files into category-based folders according to their extensions. It uses Python's `pathlib` module for filesystem operations and `shutil` to move files.

The application also handles duplicate filenames, skips directories, and reports the number of successfully moved and skipped files.

## Technologies Used

- Python 3
- pathlib
- os
- shutil
- VS Code
- Git & GitHub

## Features

- Automatically organize files by extension
- Create category folders for images, documents, code, and more
- Handle duplicate filenames without overwriting existing files
- Skip directories and symbolic links
- Validate the target directory and handle filesystem errors
- Display a summary of moved and skipped files

## Project Structure

```text
day22/
├── file_organizer.py
├── README.md
└── test_directory/
```

## How to Run

### Step 1: Open the Project

Open the `day22` folder in VS Code.

### Step 2: Create Test Files

Add sample files with different extensions inside `test_directory`.

### Step 3: Run the Script

Open the terminal and execute:

```bash
python file_organizer.py
```

### Step 4: Check the Results

Open `test_directory` and verify that the files have been moved into their respective category folders.

## Learning Outcomes

This project helped develop practical knowledge of Python filesystem operations, directory scanning, file extensions, `pathlib`, `shutil.move()`, duplicate filename handling, exception handling, and automation.

## Conclusion

The File Organizer demonstrates how Python can automate repetitive file-management tasks by organizing files into structured folders, reducing manual effort and improving file accessibility.