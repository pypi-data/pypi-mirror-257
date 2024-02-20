from abc import ABC, abstractmethod
from typing import Dict
from protkit.structure.protein import Protein

class EpitopeEvaluator(ABC):
    """
    Abstract base class for epitope evaluation, predicting the likelihood of each residue in a protein
    being part of an epitope.
    """

    def __init__(self):
        """Initialize the epitope evaluator."""
        pass

    @abstractmethod
    def predict_epitopes(self, antigen: Protein) -> Protein:
        """
        Predict the probability of each residue in the antigen to be part of an epitope.

        :param antigen: Protein object representing the 3D structure of an antigen.
        :return: An updated Protein object where each residue has an associated epitope probability.
        """
        pass
