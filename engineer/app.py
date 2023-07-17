import subprocess
from .utils import prompt_string
from .repo import RepoConfig
from .engineer import Engineer, Workspace

__all__ = ["Configuration", "run"]


class Configuration:
    def __init__(self, repo, base_branch, dev_branch, path, goal):
        self.repo = repo
        self.base_branch = base_branch
        self.dev_branch = dev_branch
        self.path = path
        self.goal = goal


def run(configuration: Configuration):
    temp_path = "./tmp/repo"

    print("GETTING READY")

try:
    subprocess.run(f"rm -r -f {temp_path}", shell=True, stdout=subprocess.PIPE)
except Exception as e:
    print(f'Error: {e}')
    subprocess.run(
        script(
            [
                f"git clone {configuration.repo} " + temp_path,
                f"cd {temp_path}",
                f"git fetch",
                f"git checkout {configuration.base_branch}",
                f"git pull origin {configuration.base_branch}",
                f"git checkout -b {configuration.dev_branch}",
                f"touch ./tmp/session.csv",
            ]
        ),
        shell=True,
        stdout=subprocess.PIPE,
try:
    subprocess.run(
        script(
            [
                f"git clone {configuration.repo} " + temp_path,
                f"cd {temp_path}",
                f"git fetch",
                f"git checkout {configuration.base_branch}",
                f"git pull origin {configuration.base_branch}",
                f"git checkout -b {configuration.dev_branch}",
                f"touch ./tmp/session.csv",
            ]
        ),
        shell=True,
        stdout=subprocess.PIPE,
    )
except Exception as e:
    print(f'Error: {e}')

    print("GETTING TO WORK")

    repo = RepoConfig(temp_path)
    workspace = Workspace(
        path=temp_path + configuration.path,
        goal=configuration.goal,
        repo_name=repo.name,
        repo_description=repo.description,
        exclude_list=repo.exclude_list,
    )
    engineer = Engineer(workspace)
try:
    engineer.execute()
except Exception as e:
    print(f'Error: {e}')

    print("FINISHED WORK")

    subprocess.run(
        script(
            [
                f"cd {temp_path}",
                f"git add .",
                "git commit -m '[GPT] Generated Suggestions\n## Goal\n{0}\n\n#### Path: {1}'".format(
                    configuration.goal, configuration.path
                ),
                f"git push origin {configuration.dev_branch} -f",
            ]
        ),
        shell=True,
        stdout=subprocess.PIPE,
try:
    subprocess.run(
        script(
            [
                f"cd {temp_path}",
                f"git add .",
                "git commit -m '[GPT] Generated Suggestions\n## Goal\n{0}\n\n#### Path: {1}'".format(
                    configuration.goal, configuration.path
                ),
                f"git push origin {configuration.dev_branch} -f",
            ]
        ),
        shell=True,
        stdout=subprocess.PIPE,
    )
except Exception as e:
    print(f'Error: {e}')

    print("SUCCESS! Generation complete.")


def script(cmds: list[str]):
    return " && ".join(cmds)
