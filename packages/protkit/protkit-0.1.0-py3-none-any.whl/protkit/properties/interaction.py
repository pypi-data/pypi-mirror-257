from protkit.structure.protein import Protein
from protkit.properties.property_setter import PropertySetter

class Interaction(PropertySetter):
    def __init__(self):
        pass

class Interface:
    def __init__(self, receptor: Protein, ligand: Protein, cut_off_distance: float = 4.5):

        self.receptor = receptor
        self.ligand = ligand
        self.cut_off_distance = cut_off_distance

        # calculate interface atoms and residues
        self.receptor_interface_atoms = []
        self.receptor_interface_resides = []
        self.ligand_interface_atoms = []
        self.ligand_interface_residues = []

    def get_from_distance(self, cut_off_distance: float = 4.5):
        pass

    def get_from_sasa(self):
        pass

