from flask import Flask, render_template, request

from exception import (
    handle_numeric_input,
    handle_division,
    handle_missing_key,
    handle_list_index,
    handle_type_error,
    handle_file_error
)


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    error_type = None

    if request.method == "POST":

        operation = request.form.get("operation")

        if operation == "numeric":

            value = request.form.get(
                "numeric_value",
                ""
            ).strip()

            response = handle_numeric_input(value)

            result = response["message"]

            if not response["success"]:
                error_type = "ValueError"

        elif operation == "division":

            first_value = request.form.get(
                "first_value",
                ""
            ).strip()

            second_value = request.form.get(
                "second_value",
                ""
            ).strip()

            response = handle_division(
                first_value,
                second_value
            )

            result = response["message"]

            if not response["success"]:

                if (
                    second_value == "0"
                    or second_value == "0.0"
                ):
                    error_type = "ZeroDivisionError"
                else:
                    error_type = "ValueError"

        elif operation == "key":

            key = request.form.get(
                "dictionary_key",
                ""
            ).strip()

            response = handle_missing_key(key)

            result = response["message"]

            if not response["success"]:
                error_type = "KeyError"

        elif operation == "index":

            index = request.form.get(
                "list_index",
                ""
            ).strip()

            response = handle_list_index(index)

            result = response["message"]

            if not response["success"]:

                try:
                    int(index)
                    error_type = "IndexError"
                except ValueError:
                    error_type = "ValueError"

        elif operation == "type":

            response = handle_type_error()

            result = response["message"]

            if not response["success"]:
                error_type = "TypeError"

        elif operation == "file":

            filename = request.form.get(
                "filename",
                ""
            ).strip()

            response = handle_file_error(filename)

            result = response["message"]

            if not response["success"]:
                error_type = "FileNotFoundError"

    return render_template(
        "index.html",
        result=result,
        error_type=error_type
    )


if __name__ == "__main__":

    app.run(debug=True)