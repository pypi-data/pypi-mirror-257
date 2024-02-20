from abc import ABC, abstractmethod
from protkit.structure.antibody import Antibody

class HumanisationEngine(ABC):
    """
    Abstract base class for an antibody humanization engine. This class
    provides an interface for the process of converting mouse-derived antibody
    sequences into sequences that are more human-like to reduce immunogenicity.
    """

    @abstractmethod
    def humanize_antibody(self, antibody: Antibody) -> Antibody:
        """
        Abstract method to humanize an antibody sequence.

        :param antibody: Antibody object containing the mouse-derived sequence to be humanized.
        :return: A new Antibody object with the humanized antibody sequence.
        """
        pass
