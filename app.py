from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

all_responses = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "ochallamonster"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def show_survey_start():
    """Select a survey."""

    return render_template("survey_start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Wipe previous responses and redirect to questions."""

    session[all_responses] = []

    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    choice = request.form['answer']

    responses = session[all_responses]
    responses.append(choice)
    session[all_responses] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question."""
    responses = session.get(all_responses)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)


@app.route("/complete")
def complete():
    """Survey completed. Redirect to the completed page."""

    return render_template("completion.html")