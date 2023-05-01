import urllib.request
from gptop.operation import Operation
from gptop.utils import llm_json


class Download(Operation):
    """
    An operation that downloads data
    from a provided url.
    """

    def __init__(self, id: str, type: str, name: str, description: str, metadata: any, schema: any):
        super().__init__(id, type, name, description, metadata, schema)

    @classmethod
    def TYPE(self):
        return "DOWNLOAD"

    def llm_modifier(self, response):
        return llm_json(response)

    def llm_message(self):
        return [
            {"role": "system", "content": """
                Given a download operation with a predefined schema and a user prompt,
                provide the download url to download based on the prompt.
                """.replace("\n", " ")},
            {"role": "system", "content": "Output in JSON format"},
            {"role": "system", "content": 'Example: {"download_url": "<URL>"}'},
            {"role": "user", "content": "Output in JSON format and nothing more."}
        ]

    def execute(self, input: any):
        download_url = input.get("download_url")
        try:
            response = urllib.request.urlopen(download_url)
            return response.read()
        except:
            return None
