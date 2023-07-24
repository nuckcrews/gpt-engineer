import os
import json
from datetime import datetime
from engineer import run, Configuration
from aws import DBTable

TASKS_TABLE = os.getenv("TASKS_TABLE")
ACCESS_TOKEN = os.getenv("PERSONAL_ACCESS_TOKEN")
BOT_NAME = os.getenv("BOT_NAME")
BOT_EMAIL = os.getenv("BOT_EMAIL")


def execute(event, context):
    table = DBTable(table_name=TASKS_TABLE, partition_key="user_id", sort_key="task_id")
    print("records", event["Records"])
    for record in event["Records"]:
        body = json.loads(record["body"])

        user_id = body["user_id"]
        task_id = body["task_id"]

        task = table.get(key_value=user_id, sort_key_value=task_id)

        if not task or task["task_status"] != "PENDING":
            continue

        repository_url = task["repository_url"]
        base_branch = task["base_branch"]
        dev_branch = task["dev_branch"]
        path = task["path"]
        goal = task["goal"]

        table.update(
            key_value=user_id,
            sort_key_value=task_id,
            attrs={
                "task_status": "RUNNING"
            }
        )

        try:
            run(
                Configuration(
                    repository_url=repository_url,
                    base_branch=base_branch,
                    dev_branch=dev_branch,
                    path=path,
                    goal=goal,
                    bot_name=BOT_NAME,
                    bot_email=BOT_EMAIL,
                    access_token=ACCESS_TOKEN,
                )
            )
            table.update(
                key_value=user_id,
                sort_key_value=task_id,
                attrs={
                    "task_status": "SUCCESS",
                    "finished_at": datetime.now().isoformat(),
                },
            )
        except Exception as e:
            table.update(
                key_value=user_id,
                sort_key_value=task_id,
                attrs={
                    "task_status": "ERROR",
                    "finished_at": datetime.now().isoformat(),
                },
            )
            raise e
