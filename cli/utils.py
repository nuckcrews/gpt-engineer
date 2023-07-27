from PyInquirer import prompt

__all__ = ["prompt_confirm", "prompt_string", "prompt_list"]

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