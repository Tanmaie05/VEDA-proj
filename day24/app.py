
import json
import random
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "day24-local-quiz-secret-key"

DATA_FILE = Path(__file__).parent / "quiz_data.json"


def load_questions():
    """Load and validate questions from the JSON file."""
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        questions = json.load(file)

    if not isinstance(questions, list) or not questions:
        raise ValueError("The question file must contain a non-empty list.")

    seen_ids = set()

    for question in questions:
        if not isinstance(question, dict):
            raise ValueError("Each question must be a JSON object.")

        required = {"id", "question", "options", "answer"}

        if not required.issubset(question):
            raise ValueError("A question is missing required fields.")

        if question["id"] in seen_ids:
            raise ValueError("Question IDs must be unique.")

        seen_ids.add(question["id"])

        if (
            not isinstance(question["question"], str)
            or not question["question"].strip()
            or not isinstance(question["options"], list)
            or len(question["options"]) < 2
            or any(not isinstance(option, str) or not option.strip()
                   for option in question["options"])
            or len(set(question["options"])) != len(question["options"])
            or question["answer"] not in question["options"]
        ):
            raise ValueError("A question contains invalid data.")

    return questions


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_quiz():
    try:
        questions = load_questions()
    except (OSError, json.JSONDecodeError, ValueError):
        return "Quiz data is missing or invalid. Check quiz_data.json.", 500

    random.shuffle(questions)

    # Store question IDs and answers in the session, not in the HTML.
    session["question_ids"] = [q["id"] for q in questions]
    session["answers"] = {}
    session["quiz_active"] = True

    return redirect(url_for("quiz"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if not session.get("quiz_active"):
        return redirect(url_for("index"))

    try:
        questions = load_questions()
    except (OSError, json.JSONDecodeError, ValueError):
        session.clear()
        return "Quiz data is missing or invalid. Check quiz_data.json.", 500

    question_map = {q["id"]: q for q in questions}
    question_ids = session.get("question_ids", [])

    if not question_ids or any(qid not in question_map for qid in question_ids):
        session.clear()
        return redirect(url_for("index"))

    answers = dict(session.get("answers", {}))
    total = len(question_ids)

    if request.method == "POST":
        try:
            current_index = int(request.form.get("index", ""))
        except ValueError:
            return "Invalid question index.", 400

        if not 0 <= current_index < total:
            return "Invalid question index.", 400

        question = question_map[question_ids[current_index]]
        selected = request.form.get("answer", "")

        if selected not in question["options"]:
            return render_template(
                "quiz.html",
                question=question,
                index=current_index,
                total=total,
                error="Please select one of the available answers."
            ), 400

        answers[str(question["id"])] = selected
        session["answers"] = answers

        if current_index + 1 < total:
            return redirect(url_for("quiz", index=current_index + 1))

        return redirect(url_for("result"))

    try:
        current_index = int(request.args.get("index", "0"))
    except ValueError:
        current_index = 0

    current_index = max(0, min(current_index, total - 1))
    question = question_map[question_ids[current_index]]

    # Prevent skipping unanswered questions.
    for previous_index in range(current_index):
        previous_id = str(question_ids[previous_index])
        if previous_id not in answers:
            return redirect(url_for("quiz", index=previous_index))

    return render_template(
        "quiz.html",
        question=question,
        index=current_index,
        total=total,
        error=None
    )


@app.route("/result")
def result():
    if not session.get("quiz_active"):
        return redirect(url_for("index"))

    try:
        questions = load_questions()
    except (OSError, json.JSONDecodeError, ValueError):
        session.clear()
        return "Quiz data is missing or invalid. Check quiz_data.json.", 500

    question_map = {q["id"]: q for q in questions}
    question_ids = session.get("question_ids", [])
    answers = session.get("answers", {})

    if (
        not question_ids
        or any(qid not in question_map for qid in question_ids)
        or any(str(qid) not in answers for qid in question_ids)
    ):
        return redirect(url_for("quiz"))

    review = []
    score = 0

    for question_id in question_ids:
        question = question_map[question_id]
        selected = answers[str(question_id)]
        correct = selected == question["answer"]

        if correct:
            score += 1

        review.append({
            "question": question["question"],
            "selected": selected,
            "answer": question["answer"],
            "correct": correct
        })

    total = len(question_ids)
    percentage = round((score / total) * 100, 2)

    session["quiz_active"] = False

    return render_template(
        "result.html",
        review=review,
        score=score,
        total=total,
        percentage=percentage
    )


if __name__ == "__main__":
    app.run(debug=True)
