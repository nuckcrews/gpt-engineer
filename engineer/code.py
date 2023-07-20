import os
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    Language,
)

__all__ = ["Code", "CodeExtractor"]


class Code():
    """
    The Code class represents a single snippet from a file. It contains the file path, the language of the code, and the content of the code snippet.
    """

    def __init__(self, file_path: str, language: Language, content: str):
        self.file_path = file_path
        self.language = language
        self.content = content

    def vect(self) -> str:
        return f"File Path: {self.file_path};\n\n{self.content})"


class CodeExtractor():
    """
    The CodeExtractor class is used to extract code from a given path. It can handle both directories and individual files. If a directory is provided, it will recursively extract code from all files in the directory and its subdirectories. Files can be excluded from extraction by adding them to the exclude_list.
    """

    def __init__(self, path: str, exclude_list: list = []):
        self.base_path = path
        self.exclude_list = exclude_list

    def extract(self, operation):
        if os.path.isdir(self.base_path):
            return self._extract_from_directory(
                path=self.base_path, operation=operation
            )
        else:
            return self._extract_from_file(path=self.base_path, operation=operation)

    def _extract_from_directory(self, path: str, operation):
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                self._extract_from_file(file_path, operation=operation)
            elif os.path.isdir(file_path):
                self._extract_from_directory(file_path, operation=operation)

    def _extract_from_file(self, path: str, operation):
        if any([path.startswith(exclude_item) for exclude_item in self.exclude_list]):
            return

        self._read_file(path, operation=operation)

    def _read_file(self, path: str, operation) -> str:
        with open(path, "r") as file:
            content = file.read()

        docs = self._splitter(path).create_documents([content])

        for doc in docs:
            operation(
                Code(
                    file_path=path,
                    language=self._language(path),
                    content=doc.page_content,
                )
            )

    def _splitter(self, file_path: str) -> RecursiveCharacterTextSplitter:
        language = self._language(file_path)
        if language is None:
            return None
        else:
            return RecursiveCharacterTextSplitter.from_language(
                language=language, chunk_size=800, chunk_overlap=0
            )

    def _language(self, file_path: str) -> Language:
        extension = file_path.split(".")[-1]
        if extension == "cpp":
            return Language.cpp
        elif extension == "go":
            return Language.GO
        elif extension == "java":
            return Language.JAVA
        elif extension == "js":
            return Language.JS
        elif extension == "php":
            return Language.PHP
        elif extension == "proto":
            return Language.PROTO
        elif extension == "py":
            return Language.PYTHON
        elif extension == "rst":
            return Language.RST
        elif extension == "rb":
            return Language.RUBY
        elif extension == "rs":
            return Language.RUST
        elif extension == "scala":
            return Language.SCALA
        elif extension == "swift":
            return Language.SWIFT
        elif extension == "md":
            return Language.MARKDOWN
        elif extension == "tex":
            return Language.LATEX
        elif extension == "html":
            return Language.HTML
        elif extension == "sol":
            return Language.SOL
        else:
            return None
