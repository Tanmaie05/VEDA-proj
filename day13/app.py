from flask import Flask, render_template, request
from prime import is_prime, generate_primes

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    primes = []

    if request.method == "POST":
        number = request.form.get("number")
        start = request.form.get("start")
        end = request.form.get("end")

        if number:
            number = int(number)
            result = f"{number} is a Prime Number" if is_prime(number) else f"{number} is Not a Prime Number"

        if start and end:
            start = int(start)
            end = int(end)
            primes = generate_primes(start, end)

    return render_template(
        "index.html",
        result=result,
        primes=primes
    )

if __name__ == "__main__":
    app.run(debug=True)