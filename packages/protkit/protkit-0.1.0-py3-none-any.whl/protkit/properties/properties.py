#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Authors:  Fred Senekal (FS)
# Contact:  fred@silicogenesis.com
# License:  GPLv3

"""
Implements class `Properties` to compute the properties of a protein.
"""

from protkit.structure.protein import Protein

from protkit.properties.chemical_class import ChemicalClass
from protkit.properties.mass import Mass
from protkit.properties.hydrophobicity import Hydrophobicity
from protkit.properties.charge import Charge
from protkit.properties.volume import Volume

class Properties:
    @staticmethod
    def assign_properties_of_protein(protein: Protein):
        # Chemical Identity
        ChemicalClass.assign_chemical_class_of_protein(protein)

        # Physiochemical Properties
        Mass.assign_mass_of_protein(protein)
        Hydrophobicity.assign_hydrophobicity_of_protein(protein)

        # Pharmacophore Properties

        # Structural Properties
        Volume.assign_volume_of_protein(protein)

