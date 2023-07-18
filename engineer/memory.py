import pandas as pd
import numpy as np
from openai.embeddings_utils import get_embedding, cosine_similarity
from .extract import Extractor, File
from .utils import announce

__all__ = [
    "Memory"
]

session_memory_path = "./tmp/session.csv"

class Work():  # This class represents a unit of work done on a file

    def __init__(self, path: str, diff: str):
        self.path = path
        self.diff = diff

    def concat(self):
        return f"Path: {self.path}\n Diff: {self.diff}"

class Memory():  # This class represents the memory of the system, storing completed work and embeddings

    def __init__(self, extractor: Extractor):
        self.extractor = extractor
        self.completed_work = []
        self.embed()

    def embed(self):
        announce("Embedding files...")

        embeddings = []
def _embed(file):  # This function embeds a file and appends it to the embeddings list
            embeddings.append(self._embedding(file))

        self.extractor.extract(_embed)

        df = pd.DataFrame(embeddings, columns=["path", "name", "embedding"])
        df.set_index("path", inplace=True)
        df.to_csv(session_memory_path)

        announce("Done embedding files.")

def add_work(self, file: File):  # This function adds a completed work to the memory
        work = Work(file.path, file.diff())
        self.completed_work.append(work)

        df = pd.read_csv(session_memory_path)
        embedding = self._embedding(file)
        df.at[file.path, "embedding"] = embedding["embedding"]
        df.to_csv(session_memory_path)

def context(self, file: File):  # This function returns the context of a file, including relevant files and completed work
        relevant_files = self._relevant_files(file)
        relevant_files_concat = "\n".join([file.concat() for file in relevant_files])
        relevant_files_message = {"role": "system", "content": f"Relevant files:\n{relevant_files_concat}"}

        completed_work_concat = "\n".join([work.concat() for work in self.completed_work])
        completed_work_message = {"role": "system", "content": f"Completed work:\n{completed_work_concat}"}

        return [relevant_files_message, completed_work_message]

def _embedding(self, file: File):  # This function returns the embedding of a file
        embedding = get_embedding(
            file.content,
            engine="text-embedding-ada-002",
            max_tokens=8000
        )

        return {
            "path": file.path,
            "name": file.name,
            "embedding": embedding
        }

def _relevant_files(self, file: File):  # This function returns the files that are most relevant to a given file
        embedding = self._embedding(file)["embedding"]
        df = pd.read_csv(session_memory_path)
        df["embedding"] = df.embedding.apply(eval).apply(np.array)
        df["similarity"] = df.embedding.apply(lambda x: cosine_similarity(x, embedding))

        paths = df.sort_values(by="similarity", ascending=False).head(3).path.tolist()

        files = []
def _add_file(path):  # This function adds a file to the files list
            files.append(path)

        for path in paths:
            if isinstance(path, str):
                Extractor(path).extract(_add_file)

        return files
