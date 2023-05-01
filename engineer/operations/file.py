import os
import json
from enum import Enum
from gptop.operation import Operation
from gptop.utils import llm_json


class FileOperationType(str, Enum):
    READ = "READ"
    WRITE = "WRITE"
    DIRECTORY = "DIRECTORY"


class File(Operation):
    """
    An operation that works with files.
    """

    def __init__(self, id: str, type: str, name: str, description: str, metadata: any, schema: any):
        super().__init__(id, type, name, description, metadata, schema)
        metadata = json.loads(metadata)
        self.req_type = metadata["type"]

    @classmethod
    def TYPE(self):
        return "FILE"

    def llm_modifier(self, response):
        return llm_json(response)

    def llm_message(self):
        return [
            {"role": "system", "content": """
                Given a file operation with a predefined schema and a user prompt,
                provide the file path, operation type based on the prompt. If it is
                a write operation, provide the content property as well.
                """.replace("\n", " ")},
            {"role": "user", "content": "Output in JSON format and nothing more."}
        ]

    def execute(self, input: any):
        path = input.get("path")
        content = input.get("content")
        try:
            if self.req_type == FileOperationType.READ:
                file = open(path, "r")
                content = file.read()
                file.close()
                return content
            elif self.req_type == FileOperationType.DIRECTORY:
                return os.listdir(path)
            elif self.req_type == FileOperationType.WRITE:
                f = open(path, "a")
                f.write(self.content)
                f.close()
                return f"Wrote to file: {path}"
            return "Could not perform operation"
        except Exception as e:
            return f"Operation failed: {str(e)}"
