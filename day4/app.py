from flask import Flask, render_template, request

app = Flask(__name__, template_folder=".")


subjects = [
    "Computer Networks",
    "Data Structures",
    "Artificial Intelligence",
    "Machine Learning",
    "Operating Systems"
]


@app.route("/")
def home():

    return render_template(
        "index.html",
        subjects=subjects
    )


@app.route("/calculate", methods=["POST"])
def calculate():

    try:

        marks = []

        # Get marks from form
        for subject in subjects:

            mark = float(request.form[subject])

            # Validate range
            if mark < 0 or mark > 100:

                return render_template(
                    "index.html",
                    subjects=subjects,
                    error=f"{subject} marks must be between 0 and 100."
                )

            marks.append(mark)


        # Calculate total and percentage
        total = sum(marks)

        percentage = total / len(subjects)


        # Grade conditions
        if percentage >= 90:
            grade = "A+"

        elif percentage >= 80:
            grade = "A"

        elif percentage >= 70:
            grade = "B"

        elif percentage >= 60:
            grade = "C"

        elif percentage >= 50:
            grade = "D"

        elif percentage >= 40:
            grade = "E"

        else:
            grade = "F"


        results = {
            "total": total,
            "percentage": percentage,
            "grade": grade
        }


        return render_template(
            "index.html",
            subjects=subjects,
            results=results
        )


    except ValueError:

        return render_template(
            "index.html",
            subjects=subjects,
            error="Please enter valid numeric marks."
        )


if __name__ == "__main__":

    app.run(debug=True)