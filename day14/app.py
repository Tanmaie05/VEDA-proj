from flask import Flask, render_template, request
from temperature import convert_temperature

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    if request.method == "POST":
        try:
            value = float(request.form["temperature"])
            from_unit = request.form["from_unit"]
            to_unit = request.form["to_unit"]

            result = round(
                convert_temperature(value, from_unit, to_unit), 2
            )

        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        result=result,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)