from typing import List
from src.core.protein import Protein

class PQRIO():
    @staticmethod
    def read(file_path: str) -> Protein:
        return Protein()

    @staticmethod
    def write(file_path: str, protien: Protein):
        with open(file_path, "wt") as file:
            file.write("")