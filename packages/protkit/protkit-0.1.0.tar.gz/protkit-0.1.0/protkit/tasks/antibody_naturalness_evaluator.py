from abc import ABC, abstractmethod
from protkit.seq.sequence import Sequence
from protkit.structure.antibody import Antibody

class AntibodyNaturalnessEvaluator(ABC):
    """
    Abstract base class for evaluating the naturalness of an antibody sequence.
    Naturalness refers to how similar an antibody sequence is to those found in nature.
    High naturalness indicates potential functionality and lower immunogenicity.
    """

    @abstractmethod
    def evaluate_naturalness(self, antibody: Antibody) -> float:
        """
        Evaluate the naturalness of an antibody sequence.

        :param antibody: An Antibody object containing the sequence to be evaluated.
        :return: A float value representing the degree of naturalness.
        """
        pass

    # OR/AND per residue value


    # OR/AND residue likelihoods
