from flask import Flask
import flask
from pathlib import Path

import util

app = Flask(__name__)


@app.route('/')
def index():
    return flask.render_template("index.html")


@app.route("/commit-log", methods=["POST"])
def commit_log():
    data = flask.request.form

    output = "<ol>"
    for commit_message in util.generate_commit_messages(data["repo-path"]):
        output += f"<li>{commit_message}</li>"
    output += "</ol>"
    return output
