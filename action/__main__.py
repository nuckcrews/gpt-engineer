"""GPT Engineer: Completes software engineering tasks for you"""
import sys
import os
import action.app as app

if __name__ == "__main__":
    print("args")
    print(sys.argv)
    repository_url = os.environ.get("GITHUB_REPOSITORY")
    access_token = os.environ.get("GITHUB_PAT")
    bot_name = os.environ.get("BOT_NAME")
    bot_email = os.environ.get("BOT_EMAIL")

    app.main(
        repository_url,
        sys.argv[1],
        sys.argv[2],
        sys.argv[3],
        sys.argv[4],
        bot_name,
        bot_email,
        access_token,
    )
