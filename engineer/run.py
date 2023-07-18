import subprocess
from .repo import RepoConfig
from .engineer import Engineer, Workspace

__all__ = ["Configuration", "run"]


class Configuration:
    """
    This class is responsible for setting up the configuration for the GPT Engineer.
    """
def __init__(self, repository_url, base_branch, dev_branch, path, goal):
        """
        Initializes the Configuration class.

        Parameters:
        repository_url (str): The URL of the repository.
        base_branch (str): The base branch of the repository.
        dev_branch (str): The development branch of the repository.
        path (str): The path to the file in the repository.
        goal (str): The goal for the GPT Engineer.
        """
        self.repository_url = repository_url
        self.base_branch = base_branch
        self.dev_branch = dev_branch
        self.path = path
        self.goal = goal


def run(configuration: Configuration):
    """
    This function runs the GPT Engineer with the given configuration.

    Parameters:
    configuration (Configuration): The configuration for the GPT Engineer.
    """
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
    workspace = Workspace(
        path=temp_path + configuration.path,
        goal=configuration.goal,
        repo_name=repo.name,
        repo_description=repo.description,
        exclude_list=repo.exclude_list,
    )
    engineer = Engineer(workspace)
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
    """
    This function joins the given commands with ' && '.

    Parameters:
    cmds (list): The list of commands to join.
    """
    return " && ".join(cmds)
