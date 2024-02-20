from abc import ABC, abstractmethod
from protkit.structure.antibody import Antibody
from protkit.seq.sequence import Sequence
from protkit.util.paratope import Paratope

class ParatopeEvaluator(ABC):
    """
    Abstract base class for a paratope evaluator that defines the interface
    for tools performing paratope prediction on antibodies, annotating the
    antibody's residues with paratope probabilities.
    """

    # TODO: There are sequence based and structured based tools. How will the interfaces differ for them?

    @abstractmethod
    def predict_paratope(self, antibody: Antibody) -> Paratope:
        """
        Annotate the antibody's residues with probabilities of being involved in antigen binding.

        :param antibody: Protein object representing the 3D structure of the antibody.
        :return: Annotated Protein object with paratope probabilities added to its residues.
        """
        pass

