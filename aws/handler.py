import os
import json
from datetime import datetime
from .db import DBTable

__all__ = ["TaskHandler"]

TASKS_TABLE = os.getenv("TASKS_TABLE")
ACCESS_TOKEN = os.getenv("PERSONAL_ACCESS_TOKEN")
BOT_NAME = os.getenv("BOT_NAME")
BOT_EMAIL = os.getenv("BOT_EMAIL")


class Bot:
    def __init__(self, name, email, access_token):
        self.name = name
        self.email = email
        self.access_token = access_token


class TaskHandler:
    def __init__(self, record):
        self.table = DBTable(
            table_name=TASKS_TABLE, partition_key="user_id", sort_key="task_id"
        )
        body = json.loads(record["body"])

        self.user_id = body["user_id"]
        self.task_id = body["task_id"]

        task = self.table.get(key_value=self.user_id, sort_key_value=self.task_id)

        if not task or task["task_status"] != "PENDING":
            raise Exception("Task not found")

        self.repository_url = task["repository_url"]
        self.base_branch = task["base_branch"]
        self.dev_branch = task["dev_branch"]
        self.path = task["path"]
        self.goal = task["goal"]
        self.bot = Bot(BOT_NAME, BOT_EMAIL, ACCESS_TOKEN)

    def task_link(self):
        link = self.repository_url.replace(".git", "/compare")
        link += f"/{self.base_branch}...{self.dev_branch}?expand=1"
        return link

    def running(self):
        self.table.update(
            key_value=self.user_id,
            sort_key_value=self.task_id,
            attrs={"task_status": "RUNNING"},
        )

    def success(self):
        self.table.update(
            key_value=self.user_id,
            sort_key_value=self.task_id,
            attrs={
                "task_status": "SUCCESS",
                "finished_at": datetime.now().isoformat(),
                "link": self.task_link(),
            },
        )

    def error(self, error):
        self.table.update(
            key_value=self.user_id,
            sort_key_value=self.task_id,
            attrs={
                "task_status": "ERROR",
                "finished_at": datetime.now().isoformat(),
                "error": str(error),
            },
        )
