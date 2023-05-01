import openai
import gptop
import os
from dotenv import load_dotenv

load_dotenv()

from .operations import ScanEdit, Command, Download, File, Exit

openai.api_key = os.getenv("OPENAI_API_KEY")

gptop.init(
    openai_key=os.getenv("OPENAI_API_KEY"),
    pinecone_key=os.getenv("PINECONE_API_KEY"),
    pinecone_region=os.getenv("PINECONE_REGION"),
    pinecone_index=os.getenv("PINECONE_INDEX"),
    operations_types=[
        ScanEdit,
        Command,
        Download,
        File,
        Exit
    ]
)
