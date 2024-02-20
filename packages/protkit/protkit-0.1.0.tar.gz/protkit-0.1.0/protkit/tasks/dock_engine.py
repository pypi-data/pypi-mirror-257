from abc import ABC, abstractmethod
from typing import List
from protkit.structure.protein import Protein
from protkit.structure.residue import Residue


class DockEngine(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def blind_dock(self, protein1: Protein, protein2: Protein) -> Protein:
        pass

    @abstractmethod
    def rigid_docking(self, protein1: Protein, protein2: Protein) -> Protein:
        pass

    def flexible_docking(self, protein1: Protein, protein2: Protein) -> Protein:
        pass

    @abstractmethod
    def information_based_docking(self, protein1: Protein, protein2: Protein, residues: List[Residue]):
        pass;