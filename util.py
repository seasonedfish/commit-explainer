from git import Repo


def generate_commit_messages(repo_path: str) -> list[str]:
    repo = Repo(repo_path)
    return [commit.message for commit in repo.iter_commits("master", max_count=50)]
