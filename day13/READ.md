# Prime Number Analyzer

## Objective
Build a program that checks whether a number is prime and generates all prime numbers within a specified range.

## Features

- Check if a number is prime
- Generate prime numbers within a range
- Flask-based web interface
- Reusable is_prime() function

## Project Structure

day13/
│
├── app.py
├── prime.py
├── README.md
│
└── templates/
    └── index.html

## How to Run

### Create Virtual Environment

python -m venv .venv

### Activate Environment

Windows:

.venv\Scripts\activate

### Install Flask

pip install flask

### Run Application

python app.py

### Open Browser

http://127.0.0.1:5000

## Algorithm

1. If the number is less than or equal to 1, it is not prime.
2. Check divisibility from 2 to √n.
3. If divisible, number is not prime.
4. Otherwise, it is prime.
5. For range generation, apply the same logic to every number.

## Time Complexity

Prime Check: O(√n)

Range Generation: O((end-start+1) × √n)
``