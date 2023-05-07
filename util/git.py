import subprocess


def clone_repo(repo_url: str, dest: str):
    result = subprocess.run(
        ["git", "clone", repo_url, dest],
        check=True,
        stderr=subprocess.PIPE,
    )

    if result.stdout:
        message = result.stdout.decode("utf-8")
        raise ValueError("Error calling git command " + message)
