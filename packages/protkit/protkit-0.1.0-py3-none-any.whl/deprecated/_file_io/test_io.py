from src.file_io.pdb_io import PDBIO

file_name_in: str = "src/test/1AHW.pdb"
file_name_out: str = "src/test/1AHW_out.pdb"

protein = PDBIO.load(file_name_in)[0]

chain = protein.get_chain('A')
# chain = list(protein.filter_chains([('chain_id', "A")]))
# residues = list(protein.filter_residues(chain_criteria=[('chain_id', "A")], residue_criteria=[('residue_type', ['GLY', 'ALA'])]))
atoms = list(protein.filter_atoms(atom_criteria=[('atom_type', ['CA', 'N', 'C'])]))

for atom in atoms:
    atom.set_attribute("is_backbone_atom", True)
# atoms = list(residue.filter_atoms([('atom_type','CA')]))
# atoms = list(residue.filter_atoms([('element','C')]))
# atoms = list(chain.filter_atoms(
#                 atom_criteria=[('atom_type', ['CA', 'O'])],
#                 residue_criteria=[('residue_type', ['GLY', 'ALA'])]
#         ))
coords = [(atom.x, atom.y, atom.z) for atom in atoms]
backbone_atoms = list(protein.filter_atoms(atom_criteria=[('is_backbone_atom', True)]))
# residues = list(chain.filter_residues([('residue_type', ['GLY', 'ALA'])]))


# PDBIO.save(file_name_out, protein)

protein_score = 5
protein.set_attribute("score", protein_score)

protein.set_attribute("x-rays", [1, 2, 3, 4])



print(protein.get_attribute("x-rays"))