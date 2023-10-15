from git import Repo
from dataclasses import dataclass


@dataclass()
class CommitMessage:
    title: str
    body: str


def generate_commit_messages(repo_path: str) -> dict[CommitMessage]:
    repo = Repo(repo_path)
    return {
        commit.hexsha: CommitMessage(
            title=commit.summary,
            body=commit.message.split(commit.summary)[1]
        )
        for commit in repo.iter_commits("master", max_count=50)
    }
