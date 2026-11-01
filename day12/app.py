from flask import Flask, render_template, request
from palindrome import check_palindrome

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    text = ""
    normalized_text = ""
    reversed_text = ""
    result = ""

    if request.method == "POST":

        text = request.form.get("text", "").strip()

        # Handle empty input
        if not text:
            result = "Please enter a word or sentence."

        else:
            is_palindrome, normalized_text, reversed_text = check_palindrome(text)

            if is_palindrome:
                result = "It is a palindrome!"
            else:
                result = "It is not a palindrome."

    return render_template(
        "index.html",
        text=text,
        normalized_text=normalized_text,
        reversed_text=reversed_text,
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)