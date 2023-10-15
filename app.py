from flask import Flask
import flask
from pathlib import Path

import util

app = Flask(__name__)


@app.route('/')
def index():
    return flask.render_template("index.html")


@app.route("/commits-explained", methods=["GET"])
def commits_explained():
    path = flask.request.args.get("repo-path")
    return flask.render_template(
        "commits-explained.html",
        commit_messages=util.generate_commit_messages(path)
    )
