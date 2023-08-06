from engineer.run import Configuration, run

__all__ = ["main"]


def main(
    repository_url,
    base_branch,
    dev_branch,
    path,
    goal,
    bot_name,
    bot_email,
    access_token,
):
    run(
        Configuration(
            repository_url=repository_url,
            base_branch=base_branch,
            dev_branch=dev_branch,
            path=path,
            goal=goal,
            bot_name=bot_name,
            bot_email=bot_email,
            access_token=access_token,
        )
    )
