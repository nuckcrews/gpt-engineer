import os
import pinecone
from openai.embeddings_utils import get_embedding
from engineer.utils import announce


class Memory:

    def __init__(self, namespace: str, exclude: list[str]):
        self.namespace = namespace
        self.exclude = exclude
        self.index = pinecone.Index(os.getenv("PINECONE_INDEX"))

    def upload(self, path: str):
        if os.path.isfile(path):
            file = open(path, "r")
            content = file.read()
            file.close()

            self.upload_file(path, content=content)
            announce(path, prefix="Stored: ")
        else:
            for root, _, files in os.walk(path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)

                    if any([file_path.startswith(exclude_item) for exclude_item in self.exclude]):
                        continue

                    file = open(file_path, "r")
                    content = file.read()
                    file.close()

                    self.upload_file(file_path, content=content)
                    announce(file_path, prefix="Stored: ")

    def upload_file(self, path: str, content: any):
        embedding = get_embedding(content,
                                  engine="text-embedding-ada-002")

        to_upsert = zip([path], [embedding])

        self.index.upsert(vectors=list(to_upsert), namespace=self.namespace)

    def get(self, prompt: str, top_k: int):
        embedding = get_embedding(prompt, engine="text-embedding-ada-002")

        result = self.index.query(
            vector=embedding,
            top_k=top_k,
            namespace=self.namespace,
            include_metadata=True
        )

        return result.get("matches")


