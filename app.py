from flask import Flask
import flask
from pathlib import Path

import util

app = Flask(__name__)


@app.route('/')
def index():
    return flask.render_template("index.html")


@app.route("/commit-log", methods=["GET"])
def commit_log():
    path = flask.request.args.get("repo-path")
    return flask.render_template(
        "commit-log.html",
        commit_messages=util.generate_commit_messages(path)
    )
