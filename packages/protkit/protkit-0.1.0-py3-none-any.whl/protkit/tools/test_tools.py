# from src.file_io.pdb_io import PDBIO
# from src.tools.reduce_adapter import ReduceAdaptor
#
# protein = PDBIO.load("src/test/huCD40.pdb")[0]
# protein2 = PDBIO.load("src/test/huCD40.pdb")[0]
# protein3 = PDBIO.load("src/test/huCD40FH.pdb")[0]
#
# # Protonation
# ra = ReduceAdaptor(reduce_bin_path="/home/claudio/software/reduce/reduce", build=True)
# protonated_protein = ra.protonate(protein)
#
# merge_test = ReduceAdaptor.merge(protein2, protein3)
#
# residues = list(protein.residues)
# protonated_residues = list(protonated_protein.residues)
# print(0)