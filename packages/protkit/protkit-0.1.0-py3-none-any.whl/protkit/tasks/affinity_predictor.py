from abc import ABC, abstractmethod
from protkit.structure.protein import Protein
from protkit.structure.antibody import Antibody

class AffinityPredictor(ABC):
    """
    Abstract base class for an affinity predictor that provides an interface
    for different affinity prediction methodologies, including specific methods
    for antibody-protein and general protein-protein interactions.
    """

    def __init__(self):
        """Initialize the affinity predictor."""
        pass

    @abstractmethod
    def predict_protein_affinity(self, protein1: Protein, protein2: Protein) -> float:
        """
        Predict the binding affinity between two protein molecules.

        :param protein1: A Protein object representing the first protein structure.
        :param protein2: A Protein object representing the second protein structure.
        :return: Predicted change in Gibbs free energy (dG) indicative of binding affinity.
        """
        pass
    @abstractmethod
    def predict_antibody_affinity(self, antibody: Antibody, protein: Protein) -> float:
        """
        Predict the binding affinity of an antibody to a protein target.

        :param antibody: An Antibody object representing the antibody structure.
        :param protein: A Protein object representing the protein target structure.
        :return: Predicted change in Gibbs free energy (dG) indicative of binding affinity.
        """
        pass


