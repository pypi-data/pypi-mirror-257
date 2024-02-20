import propka.input

from protkit.tasks.protonator import Protonator
from propka.molecular_container import MolecularContainer

class PropkaAdaptor(Protonator):
    def __init__(self):
        super().__init__()

    def protonate(self, protein):
        filename = "1234.pdb"
        molecule = MolecularContainer(None)
        propka.input.read_pdb(filename, None, molecule)





        # propka.molecular_container.MolecularContainer()
        # p = propka.protonate.Protonate()
        # p.protonate(protein)


        print("PROPKA protonation")
        # Example:
        # protonated_protein = propka_protonate(protein)
        # return protonated_protein

    def deprotonate(self, protein):
        # Placeholder for PROPKA deprotonation implementation
        print("PROPKA deprotonation")
        # Example:
        # deprotonated_protein = propka_deprotonate(protein)
        # return deprotonated_protein

