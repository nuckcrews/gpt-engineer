# This is the initialization file for the engineer module
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import openai

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")