from protkit.properties.circular_variance import CircularVariance
from protkit.properties.surface_area import SurfaceArea
from protkit.tools.freesasa_adaptor import FreeSASAAdaptor
from protkit.properties.structural_region import StructuralRegion
from protkit.core.protein import Protein
from protkit.file_io.pdb_io import PDBIO

protein = PDBIO.load("src/test/1AHW.pdb")[0]
# Circular variance
# cv = CircularVariance(radius=6.0)
# cv.calculate(protein)
# residue_list = cv.calculate_residue_property(protein)
# atom_list = cv.calculate_atom_property(protein)
# residues = list(protein.residues)
# protein.assign_list(residues, residue_list, "circular_variance_by_residue")

# protein.assign_list(atoms, atom_list, "circular_variance_by_atom")

# Surface area
# fsa = FreeSASAAdaptor()
# sa = SurfaceArea(assign_to_protein=True, surface_area_adaptor=fsa)
# sa.calculate_atom_property(protein)
# atoms = list(protein.atoms)

# Structural region
# fsa = FreeSASAAdaptor(assign_to_protein=False)
# sr = StructuralRegion(surface_area_adaptor=fsa, assign_to_protein=True)
# res = sr.calculate_structural_region(protein, receptor_chains=['A', 'B'], ligand_chains=['C'])
# residues = list(protein.residues)
#
# protein2 = PDBIO.load("src/test/1AHW.pdb")[0]
# sr2 = StructuralRegion(surface_area_adaptor=fsa, assign_to_protein=True)
# res2 = sr2.calculate_structural_region2(protein2, receptor_chains=['A', 'B'], ligand_chains=['C'])
# residues2 = list(protein2.residues)
print(protein)