import random

print("=" * 50)
print("       🎮 NUMBER GUESSING GAME")
print("=" * 50)

# Generate a random number between 1 and 100
secret_number = random.randint(1, 100)

attempts = 0

while True:

    try:
        guess = int(input("\nEnter your guess (1-100): "))

        if guess < 1 or guess > 100:
            print("❌ Please enter a number between 1 and 100.")
            continue

        attempts += 1

        if guess < secret_number:
            print("📈 Too Low! Try again.")

        elif guess > secret_number:
            print("📉 Too High! Try again.")

        else:
            print("\n🎉 Congratulations!")
            print(f"You guessed the correct number: {secret_number}")
            print(f"Number of attempts: {attempts}")
            print("=" * 50)
            break

    except ValueError:
        print("❌ Invalid input! Please enter a number.")