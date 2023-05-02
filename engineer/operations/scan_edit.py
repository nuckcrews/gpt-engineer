
import os
import os.path
from openai import ChatCompletion
from gptop import Operation
from gptop.utils import llm_json
from engineer.utils import announce


class ScanEdit(Operation):

    def __init__(self, id: str, type: str, name: str, description: str, metadata: any, schema: any):
        super().__init__(id, type, name, description, metadata, schema)

    @classmethod
    def TYPE(self):
        return "SCAN_EDIT"

    def llm_modifier(self, response):
        return llm_json(response)

    def llm_message(self):
        return [
            {"role": "system", "content": """
                Given a file operation with a predefined schema and a user prompt,
                provide the file path and goal of the file scan operation in JSON format based on the prompt.
                """.replace("\n", " ")},
            {"role": "user", "content": "Output in JSON format conforming to the schema and nothing more."}
        ]

    def execute(self, input: any):
        scan_edit(goal=input.get("goal"),
                  path=input.get("path"),
                  full_scan=True)
        return "Scan and edit complete"


def scan_edit(goal: str, path: str, full_scan: bool, repo_name: str = None, repo_description: str = None, exclude: list[str]=[]):
    if os.path.isfile(path):
        file = open(path, "r")
        content = file.read()
        file.close()

        refactored_content = refactor(
            goal=goal,
            file_name=path,
            content=content,
            repo_name=repo_name,
            repo_description=repo_description
        )

        file = open(path, "w")
        file.write(refactored_content)
        file.close()

        announce(path, prefix="Refactored: ")
    else:
        for root, _, files in os.walk(path):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                if any([file_path.startswith(exclude_item) for exclude_item in exclude]):
                    continue

                file = open(file_path, "r")
                content = file.read()
                file.close()

                refactored_content = refactor(
                    goal=goal,
                    file_name=file_name,
                    content=content,
                    repo_name=repo_name,
                    repo_description=repo_description
                )

                file = open(file_path, "w")
                file.write(refactored_content)
                file.close()

                announce(file_name, prefix="Refactored: ")

            if not full_scan:
                break


def refactor(goal: str, file_name: str, content, repo_name: str = None, repo_description: str = None):

    messages = []

    if repo_name and repo_description:
        messages.append({
            "role": "system",
            "content": "Repository Name: {0}; Repository Description: {1};".format(
                repo_name,
                repo_description
            )
        })

    messages.extend(
        [
            {"role": "system", "content": "Given content from a file in the repository, re-write it to work towards the provided goal."},
            {"role": "system", "content": "Output only the new content as it will be written into the file."},
            {"role": "system", "content": "If the file does not need changes, just output the existing content."},
            {"role": "system", "content": f"Goal: {goal}"},
            {"role": "system", "content": f"File Name: {file_name}"},
            {"role": "user", "content": content}
        ]
    )

    response = ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.0
    )

    return response["choices"][0]["message"]["content"]
