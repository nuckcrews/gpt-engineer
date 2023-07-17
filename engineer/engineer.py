import os
import json
import os.path
from openai import ChatCompletion
from .extract import Extractor, File
from .utils import announce, error

__all__ = ["Workspace", "Engineer"]


class Workspace:
    def __init__(
        self,
        path: str,
        goal: str,
        repo_name: str,
        repo_description: str,
        exclude_list: list[str] = [],
    ):
        self.path = path
        self.goal = goal
        self.repo_name = repo_name
        self.repo_description = repo_description
        self.exclude_list = exclude_list


class Engineer:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace
        self.extractor = Extractor(
            path=workspace.path, exclude_list=workspace.exclude_list
        )

    def execute(self):
try:
        self.extractor.extract(self._refactor)
    except Exception as e:
        error(f"Error while extracting: {str(e)}")

    def _refactor(self, file: File):
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
try:
            self._edit_repo_file(file, function_args["changes"])
        except Exception as e:
            error(f"Error while editing file: {str(e)}")
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
try:
            editable_file.writelines(lines)
        except Exception as e:
            error(f"Error while writing to file: {str(e)}")

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
