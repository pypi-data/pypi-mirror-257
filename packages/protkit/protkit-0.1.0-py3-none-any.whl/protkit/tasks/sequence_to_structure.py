from abc import ABC, abstractmethod
from typing import List
from protkit.structure.protein import Protein
from protkit.seq.sequence import Sequence


class SequenceToStructure(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def fold_monomer(self, sequence: Sequence) -> Protein:
        """
        Abstract method to fold a monomeric protein sequence.

        Parameters:
            sequence (Sequence): The sequence of the monomer to be folded.

        Returns:
            Protein: The folded protein structure.
        """
        pass

    @abstractmethod
    def fold_multimer(self, sequence: List[Sequence]) -> Protein:
        """
        Abstract method to fold a multimeric protein complex.

        Parameters:
            sequence (Sequence): The sequence of the multimer to be folded.

        Returns:
            Protein: The folded multimeric protein structure.
        """
        pass

    @abstractmethod
    def fold_antibody(self, h_sequence: Sequence, l_sequence: Sequence) -> Protein:
        """
        Abstract method to fold an antibody protein.

        Parameters:
            h_sequence (Sequence): The sequence of the heavy chain.
            l_sequence (Sequence): The sequence of the light chain.

        Returns:
            Protein: The folded antibody protein structure.
        """
        pass

    @abstractmethod
    def fold_nanobody(self, sequence: Sequence) -> Protein:
        """
        Abstract method to fold a nanobody sequence.

        Parameters:
            sequence (Sequence): The sequence of the nanobody to be folded.

        Returns:
            Protein: The folded nanobody structure.
        """
        pass

