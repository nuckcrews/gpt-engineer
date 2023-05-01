import subprocess
from .operations.scan_edit import scan_edit
from .utils import prompt_string, prompt_confirm

temp_path = "./tmp"


def main():
    repo = prompt_string("Repository URL:")
    base_branch = prompt_string("Base Branch:", default="mainline")
    dev_branch = prompt_string("Development Branch:", default="gpt-eng")
    path = prompt_string("Path to directory/file:", default="/")
    full_scan = prompt_confirm("Should I do a full scan?")
    goal = prompt_string("Goal:")

    print("GETTING READY")

    subprocess.run(
        f"rm -r {temp_path}/repo",
        shell=True,
        stdout=subprocess.PIPE
    )
    subprocess.run(
        script([
            f"git clone {repo} {temp_path}/repo",
            f"cd {temp_path}/repo",
            f"git fetch",
            f"git checkout {base_branch}",
            f"git pull origin {base_branch}",
            f"git checkout -b {dev_branch}"
        ]),
        shell=True,
        stdout=subprocess.PIPE
    )

    print("STARTING SCAN")

    scan_edit(
        goal=goal,
        path=temp_path + "/repo" + path,
        full_scan=full_scan
    )

    print("FINISHED SCAN")

    subprocess.run(
        script([
            f"cd {temp_path}/repo",
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
