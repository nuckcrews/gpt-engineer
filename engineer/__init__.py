import os
from dotenv import load_dotenv

try:
    load_dotenv()
except Exception as e:
    print(f'Error loading environment variables: {e}')

import openai

try:
    openai.api_key = os.getenv("OPENAI_API_KEY")
except Exception as e:
    print(f'Error setting OpenAI API key: {e}')

