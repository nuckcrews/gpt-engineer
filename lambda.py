import os
from engineer import run, Configuration
from aws.db import DBTable

TASKS_TABLE = os.getenv("TASKS_TABLE")


def execute(event, context):
    table = DBTable(TASKS_TABLE, key="user_id", sort_key="user")

    for record in event["Records"]:
        if record["eventName"] != "INSERT":
            continue
        new_image = record["dynamodb"]["NewImage"]

        status = new_image["status"]["S"]

        if status != "PENDING":
            continue

        user_id = new_image["user_id"]["S"]
        task_id = new_image["task_id"]["S"]
        repo = new_image["repo"]["S"]
        base_branch = new_image["base_branch"]["S"]
        dev_branch = new_image["dev_branch"]["S"]
        path = new_image["path"]["S"]
        goal = new_image["goal"]["S"]

        table.update(key=user_id, sort_key=task_id, attr="status", newValue="RUNNING")

        try:
            run(
                Configuration(
                    repo=repo,
                    base_branch=base_branch,
                    dev_branch=dev_branch,
                    path=path,
                    goal=goal,
                )
            )
            table.update(key=user_id, sort_key=task_id, attr="status", newValue="SUCCESS")
        except Exception as e:
            table.update(key=user_id, sort_key=task_id, attr="status", newValue="ERROR")
            raise e
