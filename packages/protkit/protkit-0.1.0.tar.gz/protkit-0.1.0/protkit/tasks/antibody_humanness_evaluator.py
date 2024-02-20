from abc import ABC, abstractmethod
from protkit.structure.antibody import Antibody

class AntibodyHumannessEvaluator(ABC):
    """
    Abstract base class for an antibody humanness evaluator that provides an interface for
    evaluating the human-likeness of antibody sequences.
    """

    @abstractmethod
    def evaluate_humanness(self, antibody: Antibody) -> float:
        """
        Evaluate the humanness score of an antibody sequence.

        :param antibody: Antibody object containing the sequence to be evaluated.
        :return: A float representing the humanness score of the antibody.
        """
        pass
