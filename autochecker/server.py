import requests
from flask import Flask, render_template, request
from furl import furl

from core.gdrive.gateway import GoogleSheetGateway
from core.scorer.gateway import MnistHTTPScorer
from core.submittion import StudentSubmission

app = Flask(__name__)

gsgateway = GoogleSheetGateway()
scorer = MnistHTTPScorer()


def build_gif_url(submission: StudentSubmission):
    if submission.accuracy > 0.5:
        tag = "success"
    else:
        tag = "failure"

    giphy_url = str(
        furl("https://api.giphy.com/v1/gifs/random").add(
            {
                "api_key": "uUOjWvgGc05rGBzVMxn1H9Eh2CptENBT",
                "tag": tag,
                "rating": "pg-13",
            }
        )
    )
    r = requests.get(giphy_url)
    return r.json()["data"]["image_original_url"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/submissions", methods=["POST"])
def new_submission():
    student_name = request.form["student_name"].strip()
    service_url = request.form["service_url"].strip()

    accuracy, errors = scorer.check_solution(service_url)
    student_submission = StudentSubmission(
        submit_id=StudentSubmission.gen_id(),
        student_name=student_name,
        service_url=service_url,
        accuracy=accuracy,
    )

    gsgateway.add_new_submission(student_submission)

    gif_url = build_gif_url(student_submission)
    return render_template(
        "submission.html", submission=student_submission, errors=errors, gif_url=gif_url
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
