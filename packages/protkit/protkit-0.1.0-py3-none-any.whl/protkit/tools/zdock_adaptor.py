from typing import List
from protkit.structure.protein import Protein
from protkit.structure.residue import Residue
from protkit.tasks.dock_engine import DockEngine


class ZDockAdaptor(DockEngine):
    """
    Adapter for the ZDock docking engine.

    This class provides concrete implementations of the docking operations
    using the ZDock software for performing protein-protein docking.
    """

    def __init__(self):
        """
        Initializes the ZDock adapter.
        """
        super().__init__()

    def rigid_docking(self, protein1: Protein, protein2: Protein) -> Protein:
        """
        Perform rigid docking using ZDock.

        :param protein1: The first protein in the docking interaction.
        :param protein2: The second protein in the docking interaction.
        :return: A new Protein object representing the ZDock rigid docked complex.
        """
        # Placeholder for integration with ZDock external tool
        print("ZDock rigid dock")
        # TODO: Insert code here to call the actual ZDock software
        #  and process the result to return a Protein object.
        return Protein()

    def information_based_docking(self, protein1: Protein, protein2: Protein, residues: List[Residue]):
        """
        Perform information-based docking using ZDock with a focus on specified residues.

        :param protein1: The first protein in the docking interaction.
        :param protein2: The second protein in the docking interaction.
        :param residues: A list of residues to guide the ZDock docking process.
        """
        # Placeholder for integration with ZDock external tool
        print("Zdock info based docking")
        # TODO: Insert code here to call the actual ZDock software using the information
        #   from the specified residues and process the result.
