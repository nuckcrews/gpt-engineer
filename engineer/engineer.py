import os
import json
import os.path
from openai import ChatCompletion
from .extract import Extractor, File
from .code import CodeExtractor, Code
from .memory import Memory
from .utils import announce, error

__all__ = ["Workspace", "Engineer"]


class Workspace():
    """
    This class represents the workspace for the Engineer tool.
    It contains all the necessary information about the repository.
    """

    def __init__(self, path: str, goal: str, repo_name: str, repo_description: str, exclude_list = []):
        self.path = path
        self.goal = goal
        self.repo_name = repo_name
        self.repo_description = repo_description
        self.exclude_list = exclude_list


class Engineer():
    """
    This class represents the Engineer tool.
    It contains the logic for scanning the codebase and making the necessary edits.
    """

    def __init__(self, workspace: Workspace):
        self.workspace = workspace
        self.extractor = Extractor(
            path=workspace.path, exclude_list=workspace.exclude_list
        )
        self.codeExtractor = CodeExtractor(
            path=workspace.path, exclude_list=workspace.exclude_list
        )
        self.memory = Memory(self.extractor, self.codeExtractor)

    def execute(self):
        file_paths = self._find_relevant_files()
        for file_path in file_paths:
            self.extractor.extract_path(file_path, self._refactor)

    def _refactor(self, file: File):
        announce(file.path, prefix="Working on: ")

        response = ChatCompletion.create(
            model="gpt-4",
            messages=self._messages(file),
            functions=self._edit_code_functions(),
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
        print("Changes:", changes)
        with open(file.path, "r") as editable_file:
            lines = editable_file.readlines()

        line_adjustment = 0
        for change in sorted(changes, key=lambda x: x['line']):
            line_number = change["line"] - 1 + line_adjustment
            content = change["content"]
            change_type = change["type"]

            if change_type == "remove":
                if len(lines) <= line_number:
                    continue
                lines.pop(line_number)
                line_adjustment -= 1
            elif change_type == "add":
                if len(lines) <= line_number:
                    lines.append(content + "\n")
                else:
                    lines.insert(line_number, content + "\n")
                    line_adjustment += 1
            elif change_type == "edit":
                if len(lines) <= line_number:
                    lines.append(content + "\n")
                else:
                    lines[line_number] = content + "\n"

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

        memory_messages = [
            {
                "role": "system",
                "content": "Relevant code:\n{0}".format(
                    self.memory.code_context(file)
                )
            }
        ]

        user_messages = [
            {"role": "user", "content": f"Goal: {self.workspace.goal}"},
            {"role": "user", "content": f"File Name: {file.name}"},
            {"role": "user", "content": file.content},
        ]

        return [*system_messages, *memory_messages, *user_messages]

    def _edit_code_functions(self):
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

    def _find_relevant_files(self) -> list:
        announce("Finding relevant code...")

        response = ChatCompletion.create(
            model="gpt-4",
            messages=self._relevant_code_messages(),
            functions=self._find_code_functions(),
            temperature=0.1,
        )

        response_message = response["choices"][0]["message"]

        print(response)

        if (
            response_message.get("function_call")
            and response_message["function_call"]["name"] == "edit_relevant_files"
        ):
            function_args = json.loads(response_message["function_call"]["arguments"])
            files = function_args["file_paths"]
            announce(files, prefix="Files to edit: ")
            return files
        else:
            error("No relevant files.")
            return []

    def _relevant_code_messages(self):
        system_messages = [
            {
                "role": "system",
                "content": "Given code from a repository, metadata about the repository, and a coding goal to achieve, select the files that should be edited to achieve the goal.",
            },
            {
                "role": "system",
                "content": "Repository Name: {0}; Repository Description: {1};".format(
                    self.workspace.repo_name, self.workspace.repo_description
                ),
            },
        ]

        memory_messages = [
            {
                "role": "system",
                "content": "Some code from the repository: {0}".format(
                    self.memory.goal_code_context(self.workspace.goal)
                )
            }
        ]

        print(memory_messages)
        user_messages = [
            {"role": "user", "content": f"Goal: {self.workspace.goal}"},
            {"role": "user", "content": f"What files should be edited to achieve the goal?"},
        ]

        return [*system_messages, *memory_messages, *user_messages]


    def _find_code_functions(self):
        return [
            {
                "name": "edit_relevant_files",
                "description": "Edits, removes, or adds content to a files based on the provided paths.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_paths": {
                            "type": "array",
                            "items": {
                                "type": "string",
                            },
                            "description": "A list of the paths of the files to edit.",
                        },
                    },
                    "required": ["file_paths"],
                },
            }
        ]