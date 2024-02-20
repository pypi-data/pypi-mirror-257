from abc import ABC, abstractmethod
from protkit.structure.protein import Protein


class RefinementEngine(ABC):
    """
    Abstract base class for structure relaxation or refinement engines.

    This class provides an interface for optimizing the conformation of a protein
    or molecular structure to achieve a lower-energy state.
    """

    def __init__(self):
        """
        Initialize the RefinementEngine.
        """
        pass

    @abstractmethod
    def relax_structure(self, protein: Protein) -> Protein:
        """
        Optimize the structure of a given protein to a lower-energy state.

        :param protein: A Protein object whose structure needs to be relaxed.
        """
        return Protein()
