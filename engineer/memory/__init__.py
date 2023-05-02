import os
import pinecone

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_REGION")
)

from .memory import *

__all__ = [
    "Memory"
]
