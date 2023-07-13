import os
import subprocess
import logging
import docx2txt
import PyPDF2
import pandas as pd
from .utils import *

__all__ = ["File", "Extractor"]


class File():

    def __init__(self, path: str, name: str, content: str):
        self.path = path
        self.name = name
        self.content = content

    def concat(self):
        return f"Path: {self.path}\n Name: {self.name}\n Content: {self.content}"

    def write(self, content: str):
        with open(self.path, "w") as f:
            f.write(content)

    def diff(self):
        return subprocess.check_output(["git", "diff", self.path]).decode("utf-8")



class Extractor():
    
    def __init__(self, path: str, exclude_list: list = []):
        self.base_path = path
        self.exclude_list = exclude_list

    def extract(self, operation: function):
        if self.is_directory():
            return self.get_directory_content(path=self.base_path, operation=operation)
        else:
            return self.extract_from_file(path=self.base_path, operation=operation)

    def file_name(self, path) -> str:
        return os.path.basename(path)

    def is_directory(self) -> bool:
        return os.path.isdir(self.base_path)

    def get_directory_content(self, path: str, operation: function):
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                self.extract_from_file(file_path, operation=operation)

    def extract_from_file(self, path: str, operation: function):
        if any([path.startswith(exclude_item) for exclude_item in self.exclude_list]):
            return

        content = ""
        if self.is_docx_file(path):
            content = self.read_docx_file(path)
        elif self.is_xlsx_file(path):
            content = self.read_xlsx_file(path)
        elif self.is_xls_file(path):
            content = self.read_xls_file(path)
        elif self.is_csv_file(path):
            content = self.read_csv_file(path)
        elif self.is_pdf_file(path):
            content = self.read_pdf_file(path)
        else:
            content = self.read_file(path)

        operation(
            File(path=path, name=self.file_name(path), content=str(self.strip(content)))
        )

    def read_file(self, path) -> str:
        try:
            with open(path, "r") as f:
                return f.read(10000)
        except FileNotFoundError:
            logging.error(f"File not found: {path}")
            return None
        except Exception as e:
            logging.error(f"Error reading file: {path}, {e}")
            return None

    def is_docx_file(self, path) -> bool:
        return path.endswith(".docx")

    def read_docx_file(self, path: str) -> str:
        try:
            return docx2txt.process(path)
        except Exception as e:
            logging.error(f"Error reading docx file: {path}, {e}")
            return None

    def is_xlsx_file(self, path) -> bool:
        return path.endswith(".xlsx")

    def read_xlsx_file(self, path: str) -> str:
        try:
            return pd.read_excel(path).to_string()
        except Exception as e:
            logging.error(f"Error reading xlsx file: {path}, {e}")
            return None

    def is_xls_file(self, path) -> bool:
        return path.endswith(".xls")

    def read_xls_file(self, path: str) -> str:
        try:
            return pd.read_excel(path).to_string()
        except Exception as e:
            logging.error(f"Error reading xls file: {path}, {e}")
            return None

    def is_csv_file(self, path) -> bool:
        return path.endswith(".csv")

    def read_csv_file(self, path: str) -> str:
        try:
            return pd.read_csv(path).to_string()
        except Exception as e:
            logging.error(f"Error reading csv file: {path}, {e}")
            return None

    def is_pdf_file(self, path) -> bool:
        return path.endswith(".pdf")

    def read_pdf_file(self, path: str) -> str:
        try:
            pdfReader = PyPDF2.PdfReader(path)
            content = ""
            for i in range(len(pdfReader.pages)):
                pageObj = pdfReader.pages[i]
                content += pageObj.extract_text()

            return content
        except Exception as e:
            logging.error(f"Error reading pdf file: {path}, {e}")
            return None

    def strip(self, content: str) -> str:
        if content is None:
            return None
        return content
