import sys
from gptop.operation import Operation
from gptop.utils import llm_response


class Exit(Operation):
    """
    Exits the current task.
    """

    def __init__(self, id: str, type: str, name: str, description: str, metadata: any, schema: any):
        super().__init__(id, type, name, description, metadata, schema)

    @classmethod
    def TYPE(self):
        return "EXIT"

    def llm_modifier(self, response):
        return llm_response(response)

    def llm_message(self):
        return [
            {"role": "system", "content": "Return <EXIT>"},
            {"role": "user", "content": "No matter what the use input it, output <EXIT>"}
        ]

    def execute(self, input: any):
        sys.exit()
