import os
import json
import subprocess
from .utils import *

__all__ = ["File", "Extractor"]


class File:
    
    def __init__(self, path: str, name: str, content):
        self.path = path
        self.name = name
        self.content = content

    def concat(self):
        return f"Path: {self.path}\n Name: {self.name}\n Content: {self.content}"

    def diff(self):
        return subprocess.check_output(["git", "diff", self.path]).decode("utf-8")


class Extractor:

    def __init__(self, path: str, exclude_list: list = []):
        self.base_path = path
        self.exclude_list = exclude_list

    def extract(self, operation):
        if os.path.isdir(self.base_path):
            return self._extract_from_directory(
                path=self.base_path, operation=operation
            )
        else:
            return self._extract_from_file(path=self.base_path, operation=operation)

    def _extract_from_directory(self, path: str, operation):
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                self._extract_from_file(file_path, operation=operation)
            elif os.path.isdir(file_path):
                self._extract_from_directory(file_path, operation=operation)

    def _extract_from_file(self, path: str, operation):
        if any([path.startswith(exclude_item) for exclude_item in self.exclude_list]):
            return

        content = self._read_file(path)
        operation(File(path=path, name=os.path.basename(path), content=content))

    def _read_file(self, path: str) -> str:
        lines_with_numbers = []
        with open(path, "r") as file:
            for line_number, line_content in enumerate(file, 1):
                lines_with_numbers.append((line_number, line_content.strip()))

        return json.dumps(lines_with_numbers)
