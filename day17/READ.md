# Task 17 - Menu-Driven Bank Account Simulator

## Objective

The Menu-Driven Bank Account Simulator is a web-based application developed using Python and Flask that simulates basic banking operations such as account creation, balance inquiry, deposits, withdrawals, and transaction history. The project is designed to strengthen understanding of functions, loops, input validation, state management, dictionaries, lists, and Flask-based web development.

## Description

Banking applications require accurate handling of account balances, deposits, withdrawals, and transaction records. Incorrect balance calculations or allowing withdrawals beyond the available balance can lead to financial inconsistencies.

This application provides a simple banking simulation where users can create an account with an initial balance, check their current balance, deposit money, withdraw money, and view their complete transaction history.

The application validates transaction amounts and prevents users from withdrawing more money than the available account balance.

The project follows a modular structure where banking operations are implemented using separate Python functions while Flask handles user interaction and web presentation.

## Technologies Used

• Python 3
• Flask
• HTML5
• CSS3
• Jinja2 Templates
• Flask Session
• VS Code
• Git & GitHub

## Features

· Bank account creation
· Account holder information
· Initial balance setup
· Balance inquiry
· Deposit money
· Withdrawal money
· Prevention of withdrawals greater than available balance
· Transaction history
· Automatic balance updates
· Transaction-wise balance tracking
· Input validation for invalid amounts
· Prevention of zero and negative transactions
· State management using Flask sessions
· User-friendly banking interface
· Dynamic data rendering using Flask and Jinja2
· Organized account data using dictionaries
· Transaction history stored using lists
· Modular banking operations using separate functions
· Responsive and clean UI design
· Fast and accurate balance calculation
· Flask-powered localhost web application
· Easy maintenance and future enhancement

## Banking Operations

### Account Creation

Users can create an account by entering their name and initial deposit amount.

### Balance Inquiry

The application displays the current account balance.

### Deposit

Users can deposit money into their account. The deposited amount is added to the current balance and recorded in transaction history.

### Withdrawal

Users can withdraw money from their account. The application checks whether sufficient balance is available before completing the withdrawal.

### Transaction History

Every successful deposit and withdrawal is stored in a transaction list along with the transaction amount and balance after the transaction.

## Validation

The application validates:

- Empty account holder name
- Invalid initial balance
- Negative initial balance
- Zero deposit
- Negative deposit
- Zero withdrawal
- Negative withdrawal
- Withdrawal greater than available balance
- Non-numeric transaction amounts

## State Management

Flask sessions are used to maintain the current account information, balance, and transaction history during the user's session.

## Project Structure

```text
day17
│
├── app.py
├── bank_account.py
├── README.md
│
└── templates
    └── index.html