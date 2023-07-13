import sys
import json
import tiktoken
from PyInquirer import prompt

__all__ = [
    "announce",
    "stream",
    "prompt_confirm",
    "prompt_string",
    "prompt_list",
    "llm_response",
    "llm_json",
    "num_tokens",
    "is_token_overflow",
]


def announce(message, prefix: str = ""):
    # Function to print a colored message
    cyan = '\033[96m'
    default = '\033[0m'
    print("{0}{1}{2}{3}".format(prefix, cyan, message, default))


def stream(message, prefix: str = ""):
    # Function to print a colored message
    cyan = '\033[96m'
    default = '\033[0m'
    print("{0}{1}{2}{3}".format(prefix, cyan, message, default), end="")
    sys.stdout.flush()


def prompt_confirm(question_message, default=True):
    # Function to prompt a confirmation question

    return prompt(
        {
            'type': 'confirm',
            'name': 'name',
            'message': question_message,
            'default': default
        }
    ).get('name')


def prompt_string(question_message, default=None):
    # Function to prompt a string input question

    return prompt(
        {
            'type': 'input',
            'name': 'name',
            'message': question_message,
            'default': default if default else ""
        }
    ).get('name')


def prompt_list(question_message, choices, default=None):
    # Function to prompt a list selection question
    return prompt(
        {
            'type': 'list',
            'name': 'name',
            'message': question_message,
            'choices': choices,
            'default': default
        }
    ).get('name')


def llm_response(obj: any) -> str:
    """
    Extracts the top result from the LLM output
    """

    try:
        # Get the content of the first choice in the LLM output
        return obj["choices"][0]["message"]["content"]
    except KeyError:
        # Return None if the required keys are not found
        return None


def llm_json(obj: any):
    """
    Extracts the top result from the LLM output
    and converts it to JSON
    """

    try:
        # Get the content of the first choice in the LLM output
        result = obj["choices"][0]["message"]["content"]
        # Convert the content to JSON and return it
        return json.loads(result)
    except (KeyError, json.JSONDecodeError):
        # Return None if the required keys are not found or if the content is not valid JSON
        return None

encoding_4 = tiktoken.encoding_for_model("gpt-4")
encoding_3_5 = tiktoken.encoding_for_model("gpt-3.5-turbo")

def num_tokens(content: str, model="gpt-4"):
    if model == "gpt-3.5-turbo":
        encoding = encoding_3_5
    else:
        encoding = encoding_4

    return len(encoding.encode(content))


def is_token_overflow(content: str, model="gpt-4"):
    if model == "gpt-3.5-turbo":
        max_tokens = 3900
    else:
        max_tokens = 8000
    return num_tokens(content, model=model) > max_tokens