import subprocess
from .repo import RepoConfig
from .engineer import Engineer, Workspace

__all__ = ["Configuration", "run"]


class Configuration:
    # This class is used to configure the repository and the goal
    def __init__(self, repository_url, base_branch, dev_branch, path, goal):
        self.repository_url = repository_url
        self.base_branch = base_branch
        self.dev_branch = dev_branch
        self.path = path
        self.goal = goal


def run(configuration: Configuration):
    # This function is used to run the configuration
    temp_path = "/tmp/repo"

    print("GETTING READY")

    subprocess.run(f"rm -r -f {temp_path}", shell=True, stdout=subprocess.PIPE)
    subprocess.run(
        script(
            [
                f"git clone {configuration.repository_url} " + temp_path,
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

    print("GETTING TO WORK")

repo = RepoConfig(temp_path)
    # This line is used to configure the repository
    workspace = Workspace(
        path=temp_path + configuration.path,
        goal=configuration.goal,
        repo_name=repo.name,
        repo_description=repo.description,
        exclude_list=repo.exclude_list,
    )
engineer = Engineer(workspace)
    # This line is used to initialize the engineer
    engineer.execute()

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
    )

    print("SUCCESS! Generation complete.")


def script(cmds):
    # This function is used to run the commands
    return " && ".join(cmds)
