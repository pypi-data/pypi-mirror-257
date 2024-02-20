from abc import ABC, abstractmethod
from typing import Dict, List
from protkit.structure.antibody import Antibody
from protkit.seq.antibody_sequence import AntibodySequence


class AntibodyAnnotator(ABC):
    """
    Abstract base class for an antibody numbering scheme annotator.

    This class provides an interface for different numbering schemes which allow for
    the standardized reference of antibody amino acid sequences.
    """

    def __init__(self):
        """Initialize the antibody annotator."""
        pass

    @abstractmethod
    def number_antibody(self, antibody_sequence: AntibodySequence) -> Antibody:
        """
        Apply a numbering scheme to an antibody sequence to facilitate identification
        of complementarity determining regions (CDRs) and framework regions.

        :param antibody_sequence: The amino acid sequence of the antibody.
        :return: An Antibody object annotated with numbering information.
        """

        antibody_sequence.set_attribute("numbering_scheme", "Kabat")
        antibody_sequence.set_attribute("IMGT_numbering", [1, 2, 3, 5, 6])
        antibody_sequence.delete_attribute("numbering_scheme")

        pass

    @abstractmethod
    def delineate_regions(self, antibody: Antibody) -> Dict[str, List[int]]:
        """
        Delineate the CDR and framework regions of the antibody based on the numbering.

        :param antibody: An Antibody object annotated with numbering information.
        :return: A dictionary with keys as region names and values as lists of position numbers.
        """
        pass
