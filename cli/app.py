import json
from engineer.run import Configuration, run
from engineer.utils import prompt_string, prompt_confirm

__all__ = ["main"]

def main():

    read_from_file = prompt_confirm("Read from file?")

    if read_from_file:
        file_path = prompt_string("File path:", default="/")
        with open(file_path, "r") as file:
            config = json.load(file)

        run(Configuration(**config))
    else:
        repository_url = prompt_string("Repository URL:")
        base_branch = prompt_string("Base Branch:", default="mainline")
        dev_branch = prompt_string("Development Branch:", default="gpt-eng")
        path = prompt_string("Path to directory/file:", default="/")
        goal = prompt_string("Goal:")

        run(
            Configuration(
                repository_url=repository_url,
                base_branch=base_branch,
                dev_branch=dev_branch,
                path=path,
                goal=goal
            )
        )
