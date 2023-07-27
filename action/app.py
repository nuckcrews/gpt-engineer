from engineer.run import Configuration, run

__all__ = ["main"]


def main(repository_url, base_branch, dev_branch, path, goal):
    run(
        Configuration(
            repository_url=repository_url,
            base_branch=base_branch,
            dev_branch=dev_branch,
            path=path,
            goal=goal,
        )
    )
