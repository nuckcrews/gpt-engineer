import os
import json
import os.path
from openai import ChatCompletion
from .extract import Extractor, File
from .utils import announce, error

__all__ = ["Workspace", "Engineer"]


class Workspace:
    """
    This class represents the workspace for the Engineer tool.
    It contains all the necessary information about the repository.
    """

    def __init__(self, path: str, goal: str, repo_name: str, repo_description: str, exclude_list = []):
        """
        Initializes the Workspace object.

        :param path: The path to the repository.
        :param goal: The goal for the Engineer tool to achieve.
        :param repo_name: The name of the repository.
        :param repo_description: The description of the repository.
        :param exclude_list: A list of files to exclude from the scan.
        """
        self.path = path
        self.goal = goal
        self.repo_name = repo_name
        self.repo_description = repo_description
        self.exclude_list = exclude_list


class Engineer:
    """
    This class represents the Engineer tool.
    It contains the logic for scanning the codebase and making the necessary edits.
    """

    def __init__(self, workspace: Workspace):
        """
        Initializes the Engineer object.

        :param workspace: The Workspace object containing information about the repository.
        """
        self.workspace = workspace
        self.extractor = Extractor(
            path=workspace.path, exclude_list=workspace.exclude_list
        )

    def execute(self):
        """
        Executes the Engineer tool.
        It extracts the necessary information from the codebase and makes the necessary edits.
        """
        self.extractor.extract(self._refactor)

    def _refactor(self, file: File):
        """
        Refactors a given file based on the goal provided.

        :param file: The file to refactor.
        """
        announce(file.path, prefix="Working on: ")

        response = ChatCompletion.create(
            model="gpt-4",
            messages=self._messages(file),
            functions=self._functions(),
            temperature=0.1,
        )

        response_message = response["choices"][0]["message"]

        if (
            response_message.get("function_call")
            and response_message["function_call"]["name"] == "edit_repo_file"
        ):
            function_args = json.loads(response_message["function_call"]["arguments"])
            self._edit_repo_file(file, function_args["changes"])
            announce(file.path, prefix="Refactored: ")
        else:
            error("No function call found in response message.")

    def _edit_repo_file(self, file: File, changes):
        """
        Edits, removes, or adds content to a file in the repository by line.

        :param file: The file to be updated.
        :param changes: A list of dictionaries representing the changes to make to the file.
        :return: None
        """
        print(changes)
        with open(file.path, "r") as editable_file:
            lines = editable_file.readlines()

        for change in changes:
            line_number = change["line"] - 1
            content = change["content"]
            change_type = change["type"]

            if change_type == "edit":
                lines[line_number] = content + "\n"
            elif change_type == "remove":
                lines[line_number] = ""
            elif change_type == "add":
                lines.insert(line_number, content + "\n")

        with open(file.path, "w") as editable_file:
            editable_file.writelines(lines)

    def _messages(self, file: File):
        system_messages = [
            {
                "role": "system",
                "content": "Given content from a file in the repository and other metadata about the repository, re-write it to work towards the provided goal.",
            },
            {
                "role": "system",
                "content": "Be sure to maintain correct indentation and style. Ensure the code is syntactically correct and valid.",
            },
            {
                "role": "system",
                "content": "Repository Name: {0}; Repository Description: {1};".format(
                    self.workspace.repo_name, self.workspace.repo_description
                ),
            },
        ]

        user_messages = [
            {"role": "user", "content": f"Goal: {self.workspace.goal}"},
            {"role": "user", "content": f"File Name: {file.name}"},
            {"role": "user", "content": file.content},
        ]

        return [*system_messages, *user_messages]

    def _functions(self):
        return [
            {
                "name": "edit_repo_file",
                "description": "Edits, removes, or adds content to a file in the repository by line.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "changes": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "line": {
                                        "type": "integer",
                                        "description": "The line number to edit, remove, or add content to.",
                                    },
                                    "content": {
                                        "type": "string",
                                        "description": "The content to edit, remove, or add to the line.",
                                    },
                                    "type": {
                                        "type": "string",
                                        "enum": ["edit", "remove", "add"],
                                        "description": "The type of change to make to the line.",
                                    },
                                },
                                "required": ["line", "content", "type"],
                            },
                            "description": "The changes to make to the file.",
                        },
                    },
                    "required": ["changes"],
                },
            }
        ]
