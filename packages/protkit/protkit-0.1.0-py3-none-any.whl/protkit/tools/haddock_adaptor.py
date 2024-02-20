from typing import List

from protkit.structure.protein import Protein
from protkit.structure.residue import Residue
from protkit.file_io.pdb_io import PDBIO
from protkit.tasks.dock_engine import DockEngine

class HaddockAdaptor(DockEngine):
    def __init__(self, use_waters: bool = True):
        self.use_waters = use_waters

        super().__init__()

    def blind_dock(self, protein1: Protein, protein2: Protein) -> Protein:
        if self.use_waters:
            print("Haddock blind dock with water")
        else:
            print("Haddock blind dock without water")

    def information_based_docking(self, protein1: Protein, protein2: Protein, residues: List[Residue]):
        print("Haddock info based docking")

    def haddock_specific_function(self):
        pass