from git import Repo
from dataclasses import dataclass
import json
import requests
import os


@dataclass()
class CommitMessage:
    ai_generated: bool
    summary: str


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


def summarize_commit(difference) -> str:
    return query_gpt(f"Summarize the code changes for this diff:\n{difference}")


def generate_commit_message(summary, difference) -> CommitMessage:
    goodness = query_gpt(f"Respond with only True or False, is {summary} a good description for this diff:\n{difference}")
    if goodness == "True":
        return CommitMessage(ai_generated=False, summary=summary)
    else:
        return CommitMessage(ai_generated=True, summary=summarize_commit(difference))
