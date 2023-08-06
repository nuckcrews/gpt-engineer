"""GPT Engineer: Completes software engineering tasks for you"""
import sys
import os
import action.app as app

if __name__ == "__main__":
    repository_url = os.environ.get('GITHUB_REPOSITORY')

    app.main(repository_url, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
