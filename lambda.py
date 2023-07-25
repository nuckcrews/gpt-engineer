import os
from engineer import run, Configuration
from aws import TaskHandler

TASKS_TABLE = os.getenv("TASKS_TABLE")
ACCESS_TOKEN = os.getenv("PERSONAL_ACCESS_TOKEN")
BOT_NAME = os.getenv("BOT_NAME")
BOT_EMAIL = os.getenv("BOT_EMAIL")


def execute(event, context):
    for record in event["Records"]:
        try:
            handler = TaskHandler(record)
            try:
                handler.running()

                run(
                    Configuration(
                        repository_url=handler.repository_url,
                        base_branch=handler.base_branch,
                        dev_branch=handler.dev_branch,
                        path=handler.path,
                        goal=handler.goal,
                        bot_name=handler.bot.name,
                        bot_email=handler.bot.email,
                        access_token=handler.bot.access_token,
                    )
                )

                handler.success()
            except Exception as e:
                handler.error(e)
                raise e
        except Exception as e:
            print("Error with task:", e)
            continue
