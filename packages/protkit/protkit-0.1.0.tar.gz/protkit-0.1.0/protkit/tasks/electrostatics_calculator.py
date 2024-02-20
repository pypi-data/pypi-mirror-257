from abc import ABC, abstractmethod
from protkit.structure.protein import Protein


class ElectrostaticsCalculator(ABC):
    """
    Abstract base class for calculating the electrostatic properties of proteins.

    This class provides the interface for electrostatic potential calculations,
    which are crucial for understanding protein interactions and biophysical characteristics.
    """

    @abstractmethod
    def calculate_electrostatic_potential(self, protein: Protein) -> Protein:
        """
        Calculate and assign the electrostatic potential to a protein object.

        :param protein: A Protein object whose electrostatic potential is to be calculated.
        :return: An updated Protein object with electrostatic potential properties added.
        """
        pass
