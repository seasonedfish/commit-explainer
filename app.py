from flask import Flask
import flask
from pathlib import Path

import util

app = Flask(__name__)


@app.route('/')
def index():
    return flask.render_template("index.html")


@app.route("/commits-explained", methods=["GET"])
async def commits_explained():
    path = flask.request.args.get("repo-path")
    commit_messages = await util.generate_commit_messages(path)
    return flask.render_template(
        "commits-explained.html",
        commit_messages=commit_messages
    )
