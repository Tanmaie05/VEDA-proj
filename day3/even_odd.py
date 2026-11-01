# =====================================================
# TASK 3 - EVEN AND ODD NUMBER CHECKER
# =====================================================

print("=" * 55)
print("          🔢 EVEN AND ODD NUMBER CHECKER")
print("=" * 55)

try:

    # Take input from user
    number = int(input("\nEnter a number: "))

    # Check whether number is even or odd
    if number % 2 == 0:
        print(f"\n✅ {number} is an EVEN number.")
    else:
        print(f"\n🔵 {number} is an ODD number.")

    print("=" * 55)

except ValueError:

    print("\n❌ Invalid input!")
    print("Please enter a valid integer.")