from engineer import run, Configuration


def execute(event, context):
    for record in event["Records"]:
        if record["eventName"] != "INSERT":
            continue
        new_image = record["dynamodb"]["NewImage"]

        repo = new_image["repo"]["S"]
        base_branch = new_image["base_branch"]["S"]
        dev_branch = new_image["dev_branch"]["S"]
        path = new_image["path"]["S"]
        goal = new_image["goal"]["S"]

        run(
            Configuration(
                repo=repo,
                base_branch=base_branch,
                dev_branch=dev_branch,
                path=path,
                goal=goal,
            )
        )
