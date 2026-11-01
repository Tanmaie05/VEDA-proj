# Personal Expense & Budget Tracker

## Objective
To develop a Python-based application that allows users to record daily expenses, organize them into categories, define monthly budgets, and generate spending summaries.

The project aims to strengthen Python programming skills through functions, collections, file handling, date/time operations, exception handling, and basic data processing.

## Description
The Personal Expense & Budget Tracker is a command-line application designed to simplify personal financial management. It allows users to add, view, edit, and delete expense records through an interactive menu.

Users can organize expenses into predefined categories such as Food, Transport, Shopping, Bills, Entertainment, Health, and Others. The application also supports custom categories, allowing users to classify expenses according to their needs.

A monthly budget feature helps users set spending limits and monitor their expenses. The spending summary calculates daily and monthly totals, provides category-wise breakdowns, and displays the remaining budget. A warning is displayed when monthly spending exceeds the defined budget.

The application uses JSON files to store expense records and monthly budgets. This ensures that information is maintained between application runs without requiring an external database.

## Technologies Used
- **Python:** Core programming language.
- **JSON:** Persistent storage for expenses and budgets.
- **datetime:** Date validation and daily/monthly calculations.
- **VS Code:** Development environment.
- **Git:** Version control.
- **GitHub:** Source code hosting.

## Features

1. **Add Expense:** Record expenses with date, amount, category, and description.
2. **View Expenses:** Display all saved expense records.
3. **Edit Expense:** Update existing expense information using its ID.
4. **Delete Expense:** Remove unwanted expense records.
5. **Category Management:** Use predefined or custom expense categories.
6. **Monthly Budget:** Set and update monthly spending limits.
7. **Spending Summary:** Calculate daily, monthly, and category-wise totals.
8. **Budget Warning:** Display remaining budget or an exceeded-budget warning.
9. **Search and Filtering:** Find expenses by date, category, or amount range.
10. **JSON Storage:** Automatically create and maintain JSON data files.
11. **Input Validation:** Validate amounts, dates, and categories.
12. **Exception Handling:** Handle invalid inputs and file-related errors.

## Project Structure

```text
Personal-Expense-Budget-Tracker/
│
├── main.py
├── expense_manager.py
├── storage.py
├── budget.py
├── utils.py
├── expenses.json
├── budgets.json
├── README.md
└── .gitignore
```

The JSON files are generated automatically when the application runs.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
```

### 2. Open the Project

Open the project folder in VS Code.

### 3. Run the Application

Make sure Python is installed, then execute:

```bash
python main.py
```

No external Python packages are required.

## Application Menu

```text
PERSONAL EXPENSE & BUDGET TRACKER

1. Add Expense
2. View All Expenses
3. Edit Expense
4. Delete Expense
5. Set Monthly Budget
6. View Spending Summary
7. Search/Filter Expenses
8. Exit
```

## Data Storage

The application uses two JSON files:

- **expenses.json:** Stores expense ID, date, amount, category, and description.
- **budgets.json:** Stores monthly budget information using the YYYY-MM format.

## Output Snapshots

Add screenshots of the following operations:

1. Main Menu
2. Add Expense
3. View All Expenses
4. Edit Expense
5. Delete Expense
6. Set Monthly Budget
7. Spending Summary
8. Budget Exceeded Warning
9. Search and Filter Expenses

## Learning Outcomes

- Understanding modular Python programming.
- Creating reusable functions.
- Working with lists and dictionaries.
- Reading and writing JSON files.
- Handling dates using datetime.
- Implementing input validation.
- Managing exceptions.
- Performing basic data processing and calculations.

## Conclusion

The Personal Expense & Budget Tracker provides a simple and effective way to manage daily expenses and monitor monthly spending. This project demonstrates practical Python programming concepts through a real-world application involving expense management, file handling, validation, and data processing.

**Project Name:** Personal Expense & Budget Tracker  
**Application Type:** CLI-Based Python Application  
**Storage:** JSON