import os
import json
import subprocess
from .utils import *

__all__ = ["File", "Extractor"]


class File:
    """
    This class represents a file in the repository.
    """

    def __init__(self, path: str, name: str, content):
        self.path = path
        self.name = name
        self.content = content

    def concat(self):
        return f"Path: {self.path}\n Name: {self.name}\n Content: {self.content}"

    def diff(self):
        return subprocess.check_output(["git", "diff", self.path]).decode("utf-8")


class Extractor():
"""
This class is responsible for extracting information from the repository.
It can handle both directories and individual files. If a directory is provided, it will recursively extract information from all files in the directory and its subdirectories. Files can be excluded from extraction by adding them to the exclude_list.
"""
    This class is responsible for extracting information from the repository.
    """

    def __init__(self, path: str, exclude_list: list = []):
        self.base_path = path
        self.exclude_list = exclude_list

def extract(self, operation, code=False):
if code:
        if os.path.isdir(self.base_path):
self._extract_code(self.base_path, operation)
            return self._extract_from_directory(
else:
                path=self.base_path, operation=operation
if os.path.isdir(self.base_path):
        else:
            return self._extract_from_file(path=self.base_path, operation=operation)

def _extract_code(self, path: str, operation):
    def _extract_from_directory(self, path: str, operation):
for filename in os.listdir(path):
        for filename in os.listdir(path):
file_path = os.path.join(path, filename)
            file_path = os.path.join(path, filename)
if os.path.isfile(file_path):
            if os.path.isfile(file_path):
self._extract_from_file(file_path, operation=operation)
                self._extract_from_file(file_path, operation=operation)
elif os.path.isdir(file_path):
            elif os.path.isdir(file_path):
self._extract_code(file_path, operation=operation)
                self._extract_from_directory(file_path, operation=operation)


def _extract_from_file(self, path: str, operation, code=False):
if any([path.startswith(exclude_item) for exclude_item in self.exclude_list]):
return
if code:

content = self._read_code(path)
        content = self._read_file(path)
else:
        operation(File(path=path, name=os.path.basename(path), content=content))
content = self._read_file(path)

operation(File(path=path, name=os.path.basename(path), content=content))
def _read_code(self, path: str) -> str:
        lines_with_numbers = []
with open(path, "r") as file:
        with open(path, "r") as file:
content = file.read()
            for line_number, line_content in enumerate(file, 1):
docs = self._splitter(path).create_documents([content])
                lines_with_numbers.append((line_number, line_content.strip()))
return docs

        return json.dumps(lines_with_numbers)
