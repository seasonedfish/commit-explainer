from __future__ import annotations

import asyncio

import aiohttp
from git import Repo
from dataclasses import dataclass
import json
import os


@dataclass()
class CommitMessage:
    ai_generated: bool
    summary: str


async def generate_commit_messages(repo_path: str):
    repo = Repo(repo_path)
    diffs = {
        commit.hexsha: repo.git.diff_tree("-p", commit.hexsha)
        for commit in repo.iter_commits("master", max_count=10)
    }
    summaries = await asyncio.gather(*(summarize_commit(diff) for _, diff in diffs.items()))
    return {
        hexsha: CommitMessage(ai_generated=True, summary=message)
        for hexsha, message in zip(diffs, summaries)
    }


async def query_gpt(prompt) -> str | None:
    # If this is throwing an error, set the environment variable OPENAI_KEY to your api key.
    # export OPENAI_KEY="your-key"
    api_key = os.environ["OPENAI_KEY"]
    endpoint = 'https://api.openai.com/v1/chat/completions'
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': prompt}]
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, headers=headers, data=json.dumps(data)) as response:
            if response.status == 200:
                response_json = await response.json()
                return response_json['choices'][0]['message']['content'].strip()
            else:
                print(f"Request failed with status {response.status}")
                return None


async def summarize_commit(difference):
    return await query_gpt(f"Provide a one line summary of the following commit described by this diff:\n{difference}")
