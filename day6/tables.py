# =====================================================
# TASK 6 - MULTIPLICATION TABLE
# =====================================================

print("=" * 50)
print("          ✖️ MULTIPLICATION TABLE")
print("=" * 50)

try:

    # Get number from user
    number = int(input("Enter a number: "))

    # Get the limit
    limit = int(input("Enter the limit: "))

    # Validate limit
    if limit <= 0:
        print("❌ Limit must be greater than 0.")

    else:

        print("\n" + "=" * 50)
        print(f"       Multiplication Table of {number}")
        print("=" * 50)

        # Generate multiplication table
        for i in range(1, limit + 1):

            result = number * i

            print(f"{number} × {i} = {result}")

        print("=" * 50)

except ValueError:

    print("❌ Invalid input!")
    print("Please enter whole numbers only.")