import subprocess
from gptop.operation import Operation
from gptop.utils import llm_response


class Command(Operation):
    """
    An operation that executes CLI commands
    in the local environment.
    """

    def __init__(self, id: str, type: str, name: str, description: str, metadata: any, schema: any):
        super().__init__(id, type, name, description, metadata, schema)

    @classmethod
    def TYPE(self):
        return "COMMAND"

    def llm_modifier(self, response):
        return llm_response(response)

    def llm_message(self):
        return [
            {"role": "system", "content": """
                Given a CLI command operation with a predefined schema and a user prompt,
                provide the command to run in the terminal based on the prompt.
                """.replace("\n", " ")},
            {"role": "user", "content": "Output the command to run and nothing more."}
        ]

    def execute(self, input: any):
        try:
            result = subprocess.run(
                input,
                shell=True,
                stdout=subprocess.PIPE
            )
            return result.stdout.decode('utf-8')
        except Exception as e:
            return f"Execution failed with error: {str(e)}"
