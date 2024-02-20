from protkit.structure.protein import Protein
from protkit.properties.property_setter import PropertySetter
from protkit.enum.element_template import ElementTemplate

class CoreProperties(PropertySetter):
    def __init__(self):
        pass

    def calculate_atom_property(self, protein: Protein) -> Protein:
        for atom in protein.atoms:
            atom.set_attribute("name", ElementTemplate.ELEMENT[atom.element]["name"])
            atom.set_attribute("int", ElementTemplate.ELEMENT[atom.element]["int"])
            atom.set_attribute("atomic_number", ElementTemplate.ELEMENT[atom.element]["atomic_number"])
            atom.set_attribute("radius", ElementTemplate.ELEMENT[atom.element]["radius"])
            atom.set_attribute("cov_radius", ElementTemplate.ELEMENT[atom.element]["cov_radius"])
            atom.set_attribute("vdw_radius", ElementTemplate.ELEMENT[atom.element]["vdw_radius"])

