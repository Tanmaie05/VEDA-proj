# =====================================================
# TASK 7 - SIMPLE PASSWORD VALIDATOR
# =====================================================

import string

print("=" * 55)
print("          🔐 SIMPLE PASSWORD VALIDATOR")
print("=" * 55)

print("\nPassword Requirements:")
print("✓ Minimum 8 characters")
print("✓ At least one uppercase character")
print("✓ At least one lowercase character")
print("✓ At least one number")
print("✓ At least one special character")

# Get password from user
password = input("\nEnter your password: ")

errors = []

# Check minimum length
if len(password) < 8:
    errors.append("Password must contain at least 8 characters.")

# Check uppercase character
if not any(char.isupper() for char in password):
    errors.append("Password must contain at least one uppercase character.")

# Check lowercase character
if not any(char.islower() for char in password):
    errors.append("Password must contain at least one lowercase character.")

# Check digit
if not any(char.isdigit() for char in password):
    errors.append("Password must contain at least one number.")

# Check special character
if not any(char in string.punctuation for char in password):
    errors.append("Password must contain at least one special character.")

print("\n" + "=" * 55)

# Display result
if len(errors) == 0:

    print("✅ Password is VALID!")
    print("Your password satisfies all the required conditions.")

else:

    print("❌ Password is INVALID!")
    print("\nRequirements not satisfied:")

    for error in errors:
        print("•", error)

print("=" * 55)