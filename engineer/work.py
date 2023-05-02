import subprocess
from .operations.scan_edit import scan_edit
from .utils import prompt_string, prompt_confirm
from .config import RepoConfig

temp_path = "./tmp/repo"


def main():
    repo = prompt_string("Repository URL:")
    base_branch = prompt_string("Base Branch:", default="mainline")
    dev_branch = prompt_string("Development Branch:", default="gpt-eng")
    path = prompt_string("Path to directory/file:", default="/")
    full_scan = prompt_confirm("Should I do a full scan?")
    goal = prompt_string("Goal:")

    print("GETTING READY")

    subprocess.run(
        f"rm -r -f {temp_path}",
        shell=True,
        stdout=subprocess.PIPE
    )
    subprocess.run(
        script([
            f"git clone {repo} " + temp_path,
            f"cd {temp_path}",
            f"git fetch",
            f"git checkout {base_branch}",
            f"git pull origin {base_branch}",
            f"git checkout -b {dev_branch}"
        ]),
        shell=True,
        stdout=subprocess.PIPE
    )

    print("STARTING SCAN")

    config = RepoConfig(temp_path)

    scan_edit(
        goal=goal,
        path=temp_path + path,
        full_scan=full_scan,
        repo_name=config.name,
        repo_description=config.description,
        exclude=config.exclude
    )

    print("FINISHED SCAN")

    subprocess.run(
        script([
            f"cd {temp_path}",
            f"git add .",
            "git commit -m '[GPT] Generated Suggestions\n## Goal\n{0}\n\n#### Path: {1}'".format(
                goal, path),
            f"git push origin {dev_branch}"
        ]),
        shell=True,
        stdout=subprocess.PIPE
    )

    print("SUCCESS! Generation complete.")


def script(cmds: list[str]):
    return " && ".join(cmds)
