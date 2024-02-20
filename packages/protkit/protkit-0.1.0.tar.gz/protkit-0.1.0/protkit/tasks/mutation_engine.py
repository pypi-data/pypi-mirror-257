from abc import ABC, abstractmethod
from protkit.structure.protein import Protein
from protkit.util.mutation import Mutation


class MutationEngine(ABC):
    """
    Abstract base class for a mutation engine.

    A mutation engine is responsible for applying mutations to proteins. It defines
    a common interface for various mutation implementations that can be plugged into
    the system to provide the functionality of mutating proteins.
    """

    def __init__(self):
        """
        Initializes the MutationEngine.

        Any initialization that is common to all MutationEngines can be done here,
        although as an abstract class, there might not be any concrete implementation.
        """
        pass

    @abstractmethod
    def mutate(self, protein: Protein, mutation: Mutation) -> Protein:
        """
        Abstract method for mutating a protein.

        This method should be overridden by subclasses to provide the specific
        mechanism by which a protein is mutated according to a given mutation.

        Parameters:
            protein (Protein): The protein to be mutated.
            mutation (Mutation): The mutation to be applied to the protein.

        Returns:
            Protein: A new protein instance with the mutation applied.
        """
        pass
