
import os
import os.path
from openai import ChatCompletion
from .extract import Extractor, File
from .memory import Memory, Work
from .utils import announce

__all__ = [
    "Workspace",
    "Engineer"
]

class Workspace():

    def _init__(self, path: str, goal: str, repo_name: str, repo_description: str, exclude_list: list[str]=[]):
        self.path = path
        self.goal = goal
        self.repo_name = repo_name
        self.repo_description = repo_description
        self.exclude_list = exclude_list


class Engineer():

    def __init__(self, workspace: Workspace):
        self.workspace = workspace
        self.extractor = Extractor(path=workspace.path, exclude_list=workspace.exclude_list)
        self.memory = Memory(self.extractor)

    def execute(self):
        self.extractor.extract(self._refactor)

    def _messages(self, file: File):
        system_messages = [
            {"role": "system", "content": "Given content from a file in the repository, re-write it to work towards the provided goal."},
            {"role": "system", "content": "Output only the new content as it will be written into the file."},
            {"role": "system", "content": "If the file does not need changes, just output the existing content."},
            {"role": "system", "content": "Repository Name: {0}; Repository Description: {1};".format(self.workspace.repo_name, self.workspace.repo_description)},
            {"role": "system", "content": f"Goal: {self.workspace.goal}"},

        ]
        memory_messages = self.memory.context(file)
        user_messages = [
            {"role": "system", "content": f"File Name: {file.name}"},
            {"role": "user", "content": file.content}
        ]
        return [
            *system_messages,
            *memory_messages,
            *user_messages
        ]

    def _refactor(self, file: File):
        announce(self.workspace.path, prefix="Working on: ")

        response = ChatCompletion.create(
            model="gpt-4",
            messages=self._messages(file),
            temperature=0.0
        )

        content = response["choices"][0]["message"]["content"]

        file.write(content)
        self.memory.add_work(file)

        announce(self.workspace.path, prefix="Refactored: ")

