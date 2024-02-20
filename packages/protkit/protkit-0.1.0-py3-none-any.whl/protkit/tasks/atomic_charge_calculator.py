from abc import ABC, abstractmethod
from protkit.structure.protein import Protein


class AtomicChargeCalculator(ABC):
    """
    Abstract base class for calculating atomic charges on proteins.

    This class defines the interface for tools that can assign atomic charges
    to protein structures, typically as a preparatory step for electrostatic potential
    calculations.
    """

    @abstractmethod
    def calculate_atomic_charges(self, protein: Protein) -> Protein:
        """
        Calculate and assign atomic charges to a protein structure.

        :param protein: A Protein object to assign atomic charges to.
        :return: An updated Protein object with atomic charges added.
        """
        return Protein()
