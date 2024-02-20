from abc import ABC, abstractmethod
from typing import *

from protkit.structure.protein import Protein

class PropertySetter(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def calculate_residue_property(self, protein: Protein) -> List:
        pass

    @abstractmethod
    def calculate_atom_property(self, protein: Protein) -> List:
        pass
