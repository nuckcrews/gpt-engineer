import sys
import json
import tiktoken
from PyInquirer import prompt

__all__ = [
    "announce",
    "error",
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
    """
    Function to print a colored message.
    
    Parameters:
    message (str): The message to be printed.
    prefix (str): An optional prefix for the message. Default is an empty string.
    """
    # Function to print a colored message
    cyan = '\033[96m'
    default = '\033[0m'
    print("{0}{1}{2}{3}".format(prefix, cyan, message, default))

def error(message, prefix: str = ""):
    """
    Function to print a colored error message.
    
    Parameters:
    message (str): The error message to be printed.
    prefix (str): An optional prefix for the message. Default is an empty string.
    """
    # Function to print a colored message
    red = '\033[91m'
    default = '\033[0m'
    print("{0}{1}{2}{3}".format(prefix, red, message, default))


def stream(message, prefix: str = ""):
    """
    Function to print a colored message without a newline at the end.
    
    Parameters:
    message (str): The message to be printed.
    prefix (str): An optional prefix for the message. Default is an empty string.
    """
    # Function to print a colored message
    cyan = '\033[96m'
    default = '\033[0m'
    print("{0}{1}{2}{3}".format(prefix, cyan, message, default), end="")
    sys.stdout.flush()


def prompt_confirm(question_message, default=True):
    """
    Function to prompt a confirmation question.
    
    Parameters:
    question_message (str): The question to be asked.
    default (bool): The default answer if none is provided. Default is True.
    """
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
    """
    Function to prompt a string input question.
    
    Parameters:
    question_message (str): The question to be asked.
    default (str): The default answer if none is provided. Default is None.
    """
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
    """
    Function to prompt a list selection question.
    
    Parameters:
    question_message (str): The question to be asked.
    choices (list): The list of choices.
    default (str): The default choice if none is selected. Default is None.
    """
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
    Function to extract the top result from the LLM output.
    
    Parameters:
    obj (any): The LLM output.
    
    Returns:
    str: The top result from the LLM output.
    """
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
    Function to extract the top result from the LLM output and convert it to JSON.
    
    Parameters:
    obj (any): The LLM output.
    
    Returns:
    dict: The top result from the LLM output converted to JSON.
    """
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
    """
    Function to calculate the number of tokens in the content for a specific model.
    
    Parameters:
    content (str): The content to be tokenized.
    model (str): The model to be used for tokenization. Default is "gpt-4".
    
    Returns:
    int: The number of tokens in the content.
    """
    if model == "gpt-3.5-turbo":
        encoding = encoding_3_5
    else:
        encoding = encoding_4

    return len(encoding.encode(content))


def is_token_overflow(content: str, model="gpt-4"):
    """
    Function to check if the number of tokens in the content exceeds the maximum limit for a specific model.
    
    Parameters:
    content (str): The content to be checked.
    model (str): The model to be used for checking. Default is "gpt-4".
    
    Returns:
    bool: True if the number of tokens exceeds the maximum limit, False otherwise.
    """
    if model == "gpt-3.5-turbo":
        max_tokens = 3900
    else:
        max_tokens = 8000
    return num_tokens(content, model=model) > max_tokens