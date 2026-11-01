from flask import Flask, render_template, request
import random

app = Flask(__name__, template_folder=".")

# Generate the number when the application starts
secret_number = random.randint(1, 100)

attempts = 0


@app.route("/")
def home():

    return render_template(
        "index.html",
        attempts=attempts
    )


@app.route("/guess", methods=["POST"])
def guess_number():

    global attempts

    try:

        guess = int(request.form["guess"])

        if guess < 1 or guess > 100:

            return render_template(
                "index.html",
                message="Please enter a number between 1 and 100.",
                message_type="error",
                attempts=attempts,
                guess=guess
            )

        attempts += 1

        if guess < secret_number:

            message = "📈 Too Low! Try again."
            message_type = "low"

        elif guess > secret_number:

            message = "📉 Too High! Try again."
            message_type = "high"

        else:

            message = (
                f"🎉 Congratulations! You guessed the number "
                f"{secret_number} in {attempts} attempts!"
            )

            message_type = "correct"

        return render_template(
            "index.html",
            message=message,
            message_type=message_type,
            attempts=attempts,
            guess=guess
        )

    except ValueError:

        return render_template(
            "index.html",
            message="❌ Please enter a valid number.",
            message_type="error",
            attempts=attempts
        )


@app.route("/reset")
def reset_game():

    global secret_number, attempts

    secret_number = random.randint(1, 100)
    attempts = 0

    return render_template(
        "index.html",
        message="🔄 New game started! Guess a number between 1 and 100.",
        message_type="info",
        attempts=attempts
    )


if __name__ == "__main__":
    app.run(debug=True)