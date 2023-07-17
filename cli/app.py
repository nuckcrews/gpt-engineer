from engineer.app import Configuration, run
from engineer.app import prompt_string


def main():
    repo = prompt_string("Repository URL:")
    base_branch = prompt_string("Base Branch:", default="mainline")
    dev_branch = prompt_string("Development Branch:", default="gpt-eng")
    path = prompt_string("Path to directory/file:", default="/")
    goal = prompt_string("Goal:")

    run(
        Configuration(
            repo=repo,
            base_branch=base_branch,
            dev_branch=dev_branch,
            path=path,
            goal=goal,
        )
    )
