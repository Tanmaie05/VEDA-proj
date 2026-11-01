# =====================================================
# TASK 2 - SIMPLE CALCULATOR
# =====================================================

print("=" * 55)
print("              🧮 SIMPLE CALCULATOR")
print("=" * 55)

# Functions for arithmetic operations

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "Error: Cannot divide by zero!"
    return a / b


def modulus(a, b):
    if b == 0:
        return "Error: Cannot calculate modulus with zero!"
    return a % b


# Taking input from the user

try:
    num1 = float(input("\nEnter the first number: "))
    num2 = float(input("Enter the second number: "))

    print("\n" + "=" * 55)
    print("                 CALCULATION RESULTS")
    print("=" * 55)

    # Performing operations

    print(f"➕ Addition       : {add(num1, num2)}")
    print(f"➖ Subtraction    : {subtract(num1, num2)}")
    print(f"✖️ Multiplication : {multiply(num1, num2)}")
    print(f"➗ Division       : {divide(num1, num2)}")
    print(f"％ Modulus        : {modulus(num1, num2)}")

    print("=" * 55)
    print("        ✅ All operations completed!")
    print("=" * 55)

except ValueError:
    print("\n❌ Invalid input! Please enter numeric values.")