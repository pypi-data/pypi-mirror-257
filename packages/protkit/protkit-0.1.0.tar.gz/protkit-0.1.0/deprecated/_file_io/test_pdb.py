from src.file_io.pdb_io import PDBIO
from src.file_io.prot_io import ProtIO
from src.core.protein import Protein

def process_pdb(item):
    # print(item["i"], item["file_name"])
    protein = PDBIO.load(item["file_name"])[0]
    # protein.fix_disordered_atoms()
    # protein.remove_hetero_residues()
    print(item["i"], item["file_name"], "\n", protein.summary())

def process_all_pdbs():
    import os
    import glob

    pdbs = glob.glob("/home/fred/SilicoGenesis/Repo/data/rcsb/pdb/raw/*.pdb")
    pdbs.sort()

    for i, pdb in enumerate(pdbs[:1000]):
        # print(i, pdb)
        protein = process_pdb({"i": i, "file_name": pdb})
        # ProtIO.save(pdb.replace(".pdb", ".prot"), protein)

def process_all_pdbs_in_parallel():
    import glob
    from joblib import Parallel, delayed

    pdbs = glob.glob("/home/fred/SilicoGenesis/Repo/data/rcsb/pdb/raw/*.pdb")
    pdbs.sort()
    items = [{"i": i, "file_name": pdb} for i, pdb in enumerate(pdbs[:1000])]

    Parallel(n_jobs=10)(delayed(process_pdb)(item) for item in items)

def test_disordered_atoms():
    protein = PDBIO.load("src/test/6BOM.pdb")[0]
    print(protein.summary())
    protein.fix_disordered_atoms()
    print(protein.summary())
    protein.remove_hetero_residues()
    print(protein.summary())

def what():
    # protein = PDBIO.load("/home/fred/SilicoGenesis/Repo/data/rcsb/pdb/raw/1AO2.pdb")[0]
    protein = PDBIO.load("/home/fred/SilicoGenesis/Repo/data/rcsb/pdb/raw/1AHW.pdb")[0]
    protein.get_chain("A").get_residue(0).get_atom("N").set_attribute("cool_factor", 100)
    protein.get_chain("A").set_attribute("notes", "Remember to buy milk")
    protein.get_chain("A").set_attribute("values", [1, 2, 3, 4, 5])
    print(protein.summary())
    protein.keep_chains(["A"])
    protein.remove_chains(["B"])
    protein2 = protein.copy(keep_chain_ids=["A"])
    ProtIO.save("src/test/1AHW.prot", protein, compress=False)

    protein2 = ProtIO.load("src/test/1AHW.prot", decompress=False)[0]
    print(protein.get_chain("A").get_residue(0).get_atom("N").get_attribute("cool_factor"))

    PDBIO.save("src/test/1AHW_out.pdb", protein2)


    # protein.remove_hetero_residues()
    # print(protein.summary())


# process_all_pdbs()
# process_all_pdbs_in_parallel()

# what()

# compress = False
#
# protein = PDBIO.load("src/test/1AHW.pdb")[0]
#
# ProtIO.save("src/test/1AHW.prot", protein, compress=compress)

# protein2 = protein.copy(keep_chain_ids=["A"])
#
# for chain in protein.chains:
#     count = chain.num_residues_by_type
#     print(count)

# protein.get_chain("A").chain_id = "X"
# protein2.get_chain("A").chain_id = "Y"
#
# protein.pdb_id = "N"
# protein2.pdb_id = "M"
#
# print(protein.get_chain("A").chain_id)
# print(protein2.get_chain("A").chain_id)
#
# print(protein.pdb_id)
# print(protein2.pdb_id)

# ProtIO.save("src/test/1AHW.prot", protein, compress=compress)
# protein = ProtIO.load("src/test/1AHW.prot", decompress=compress)[0]


def quick_start_example():
    from src.io.PDBIO import PDBIO

    protein = PDBIO.load("src/test/1AHW.pdb")[0]
    print(protein.chain_ids)
    print(protein.num_residues)
    print(protein.get_chain("A").num_residues)
    print(protein.get_chain("B").num_residues)

    protein.remove_chains("B")
    print(protein.chain_ids)

    # PDBIO.save("src/test/1AHW_out.pdb", protein)

    PDBIO.save(protein, "1AHW_chain_A.pdb")

def quick_start_example2():
    from src.io.ProtIO import ProtIO
    from src.io.PDBIO import PDBIO

    protein = PDBIO.load("src/test/1AHW.pdb")[0]
    protein2 = PDBIO.load("src/test/4NKQ.pdb")[0]

    print(protein.summary())
    print(protein2.summary())

    ProtIO.save([protein, protein2], "src/test/1AHW_4NKQ.prot", compress=False)
    protein, protein2 = ProtIO.load("src/test/1AHW_4NKQ.prot", decompress=False)

    print(protein.summary())
    print(protein2.summary())

    # from src.io.ProtIO import ProtIO
    #
    # protein = ProtIO.load("src/test/1AHW.prot", decompress=True)[0]
    # ProtIO.save(protein, "src/test/1AHW_json.prot", compress=False)


def example3():
    from src.io.ProtIO import ProtIO

    ProtIO.convert("src/test/1AHW.pdb", "src/test/1AHW.prot", compress=True)
    protein = ProtIO.load("src/test/1AHW.prot")[0]

    for chain in protein.chains:
        print(f"{chain.chain_id}: {chain.num_residues} residues")
        print(chain.sequence)

def example4():
    from src.io.ProtIO import ProtIO
    protein = ProtIO.load("src/test/1AHW.prot")[0]

    coordinates = [(atom.x, atom.y, atom.z) for atom in protein.get_chain("A").atoms]
    print(coordinates)

def example5():
    from src.io.ProtIO import ProtIO
    protein = ProtIO.load("src/test/1AHW.prot")[0]

    atoms = protein.filter_atoms(residue_criteria=[("residue_type", "PRO")], atom_criteria=[("atom_type", ["C", "CA", "N"])])
    for atom in atoms:
        print(f"{atom.residue.residue_code}, {atom.atom_type}, {atom.x}, {atom.y}, {atom.z}")


# quick_start_example()
# quick_start_example2()
example5()
