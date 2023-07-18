import os  # Importing os module to interact with the OS
from dotenv import load_dotenv  # Importing load_dotenv from dotenv to load environment variables

load_dotenv()  # Loading environment variables

import openai  # Importing openai to interact with OpenAI's API

openai.api_key = os.getenv("OPENAI_API_KEY")  # Setting OpenAI's API key from environment variable

from .run import *  # Importing all from run module

__all__ = ["run", "Configuration"]  # Defining all the modules to be imported when * is used
