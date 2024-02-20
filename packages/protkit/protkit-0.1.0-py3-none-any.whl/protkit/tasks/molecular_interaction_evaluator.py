from abc import ABC, abstractmethod
from typing import Tuple
from protkit.structure.protein import Protein

class MolecularInteractionEvaluator(ABC):
    """
    Abstract base class for evaluating molecular interactions, particularly between proteins.
    """

    def __init__(self):
        """Initialize the molecular interaction evaluator."""
        pass

    @abstractmethod
    def calculate_interactions(self, protein1: Protein, protein2: Protein) -> Tuple[Protein, Protein]:
        """
        Calculate and annotate the interactions between two proteins. The interactions are
        directly annotated onto the atoms and residues within each Protein object.

        :param protein1: The first protein involved in the interaction.
        :param protein2: The second protein involved in the interaction.
        :return: A tuple of two Protein objects with updated interaction annotations.
        """
        pass
