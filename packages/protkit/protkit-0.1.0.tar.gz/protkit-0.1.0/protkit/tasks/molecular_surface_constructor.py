from abc import ABC, abstractmethod
from protkit.structure.protein import Protein
from protkit.util.surface import Surface


class MolecularSurfaceConstructor(ABC):
    """
    Abstract base class for constructing the molecular surface of a protein.

    The molecular surface is defined as the surface that represents the boundary
    between the protein and its solvent. This surface is crucial for understanding
    various physicochemical properties of the protein and its interactions with other
    molecules.

    The implementing classes should provide functionality to generate this surface
    based on the atomic coordinates and radii present in the Protein instance.

    The output is expected to be a Surface object enriched with surface information, which
    could include surface vertices, normals, and areas.
    """

    def __init__(self):
        """
        Initializes the MolecularSurfaceConstructor.
        """
        pass

    @abstractmethod
    def construct_surface(self, protein: Protein) -> Surface:
        """
        Abstract method to construct the molecular surface of a given protein.

        This method should analyze the three-dimensional structure of the protein,
        considering the atomic coordinates and atomic radii, to produce a detailed
        representation of the molecular surface.

        Parameters:
        - protein: Protein instance for which the surface will be constructed.

        Returns:
        - A new Surface instance that includes the molecular surface information.
        """
        pass
