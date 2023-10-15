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
    return flask.render_template(
        "commit-log.html",
        commit_messages=util.generate_commit_messages(data["repo-path"])
    )
