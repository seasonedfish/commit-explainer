from git import Repo
from dataclasses import dataclass
import json
import requests
import os


@dataclass()
class CommitMessage:
    ai_generated: bool
    title: str
    body: str


def generate_commit_messages(repo_path: str) -> dict[CommitMessage]:
    repo = Repo(repo_path)
    return {
        commit.hexsha: generate_commit_message(commit.summary, repo.git.diff(commit.hexsha, "-p"))
        for commit in repo.iter_commits("master", max_count=2)
    }


def query_gpt(prompt) -> str:
    # If this is throwing an error, set the environment variable OPENAI_KEY to your api key.
    # export OPENAI_KEY="your-key"
    api_key = os.environ["OPENAI_KEY"]
    endpoint = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': prompt}]
    }
    response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code}"


def good_commit(difference):
    return query_gpt('Summarize the code diff in a medium sized paragraph' + difference)


def bad_commit(difference):
    return query_gpt('Summarize the code diff in a 8 words or less' + difference), query_gpt(
        'Summarize the code diff in a medium sized paragraph ' + difference)


def generate_commit_message(message, difference) -> CommitMessage:
    goodness = query_gpt('respond with only True or False, is' + message + 'a good description for' + difference)
    if goodness == "True":
        return CommitMessage(True, message, good_commit(difference))
    else:
        return CommitMessage(False, *bad_commit(difference))
