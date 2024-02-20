"""
The SurfaceArea class provides functionality to compute protein surface areas.

The ASA or SASA was first described by Lee and Richards in 1971. Shrake and Rupley
developed the rolling ball algorithm in 1973.

RASA can be calculated by dividing the ASA by the MaxASA. MasASA values were calculated
by Miller et al. (1987).

Levy (2010) describes a method for defining interior, surface, support, core and rim
residues of a protein based on ASA calculations.

Abbreviations:
--------------

ASA    - Accessible Surface Area
BASA   - Buried Surface Area
MaxASA - Maximum Accessible Surface Area
RASA   - Relative Accessible Surface Area = ASA / MaxASA
SASA   - Solvent Accessible Surface Area (same as ASA)

Papers referenced in this code:
-------------------------------

Lee B., Richards F.M. (1971)
The interpretation of protein structures: estimation of static accessibility.
J. Mol. Biol. Vol. 55, pp. 279-400.

Levy E.D. (2010)
A simple definition of structural regions in proteins and its use in analyzing
interface evolution.
J. Mol. Biol. Vol. 403, pp. 660-670.

Miller S., Janin J., Lesk A.M., Chothia C. (1987).
Interior and surface of monomeric proteins.
J. Mol. Biol. Vol. 196, pp. 641-656.

Mitternacht S. (2016)
FreeSASA: An open source C library for solvent accessible surface area calculations.
F1000 Research, 5:189.

Shrake A., Rupley J.A. (1973)
Environment and exposure to solvent of protein atoms. Lysozyme and insulin.
J. Mol. Biol. Vol. 79, pp. 351-371.

External packages used in this code:
------------------------------------

FreeSASA - https://freesasa.github.io/
Provides C implementations of the Lee-Richards and Shrake-Rupley algorithms
with implementation hooks for Python.

"""

import numpy as np
from typing import *

from protkit.structure.protein import Protein
from protkit.properties.property_setter import PropertySetter
from protkit.tasks.surface_area_calculator import SurfaceAreaCalculator

class SurfaceArea(PropertySetter):
    def __init__(self, surface_area_adaptor: SurfaceAreaCalculator):
        # Maximum ASA as determined by Miller et al. (1987)
        # This is the maximum possible surface area per amino acid.
        self._surface_area_adaptor = surface_area_adaptor


    def calculate_atom_property(self, protein: Protein) -> List:
        """
        Calculate the surface areas of a protein using FreeSASA and optionally update the protein object.

        :param protein: A Protein object whose surface area needs to be calculated.
        :return: A Dict object with new surface area properties.
        """
        atom_bound_surface_areas = self._surface_area_adaptor.calculate_surface_area(protein)

        return atom_bound_surface_areas

    def calculate_residue_property(self, protein: Protein) -> Dict:
        pass
