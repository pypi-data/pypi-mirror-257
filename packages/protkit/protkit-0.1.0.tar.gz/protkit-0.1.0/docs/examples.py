class Examples:
    @staticmethod
    def copy_protein():
        from src.file_io.prot_io import ProtIO
        protein = ProtIO.load("3i40.prot")[0]
        protein2 = protein.copy()
        protein2.save("3i40_copy.prot")

    @staticmethod
    def remove_water():
        from src.file_io.prot_io import ProtIO
        # ProtIO.convert("6BOM.pdb", "6BOM.prot")
        protein = ProtIO.load("6BOM.prot")[0]
        print(f"{protein.num_water_residues}")
        protein.remove_water_residues()
        print(f"{protein.num_water_residues}")

    @staticmethod
    def remove_heteroatoms():
        from src.file_io.prot_io import ProtIO
        protein = ProtIO.load("6BOM.prot")[0]
        print(f"{protein.num_hetero_residues}")
        protein.remove_hetero_residues("TRS")
        print(f"{protein.num_hetero_residues}")

    @staticmethod
    def fix_disordered_atoms():
        from src.file_io.prot_io import ProtIO
        protein = ProtIO.convert("3i40.pdb", "3i40.prot")
        print(f"{protein.num_disordered_atoms}")
        print(protein.get_chain("A").get_residue(13).is_disordered)
        print(protein.get_chain("A").get_residue(13).get_atom("CA").is_disordered)
        print(protein.get_chain("A").get_residue(13).get_atom("CB").is_disordered)
        protein.fix_disordered_atoms()
        print(protein.get_chain("A").get_residue(13).get_atom("CB").is_disordered)
        print(f"{protein.num_disordered_atoms}")

    @staticmethod
    def remove_hydrogen_atoms():
        from src.file_io.prot_io import ProtIO
        protein = ProtIO.convert("1A4Y_A_B.pdb", "1A4Y_A_B.prot")
        # protein = ProtIO.open("3i40.prot")[0]
        print(f"{protein.num_atoms} atoms")
        print(f"{protein.num_heavy_atoms} heavy atoms")
        print(f"{protein.num_hydrogen_atoms} hydrogen atoms")
        protein.remove_hydrogen_atoms()
        print(f"{protein.num_hydrogen_atoms} hydrogen atoms after removal")

    @staticmethod
    def remove_atoms():
        from src.file_io.prot_io import ProtIO
        protein = ProtIO.load("3i40.prot")[0]
        residue = protein.get_chain("A").get_residue(2)

        print(f"{residue.num_atoms} atoms before removal")

        residue.remove_atoms(["CB", "CG1", "CG2"])

        print(f"{residue.num_atoms} atoms after removal")

    @staticmethod
    def keep_backbone_atoms():
        from src.file_io.prot_io import ProtIO
        protein = ProtIO.load("3i40.prot")[0]

        print(f"{protein.num_atoms} atoms")

        protein.keep_backbone_atoms()

        print(f"{protein.num_atoms} atoms in backbone")

    @staticmethod
    def missing_or_extra_atoms():
        from src.file_io.prot_io import ProtIO
        protein = ProtIO.load("1A4Y_A_B.prot")[0]

        protein.remove_hetero_residues()
        print(protein.anomaly_report())

    @staticmethod
    def seqres_records():
        from src.file_io.prot_io import ProtIO
        # protein = PDBIO.load("3i40.pdb", pdb_id="3i40")[0]
        protein = PDBIO.load("4nkq.pdb", pdb_id="4nkq")[0]
        protein.get_chain("A").seqres_analysis()
        protein.get_chain("B").seqres_analysis()
        protein.get_chain("C").seqres_analysis()
        protein.get_chain("A").assign_segments()
        print(protein.num_chains)

    @staticmethod
    def set_get_attribute():
        from src.file_io.prot_io import ProtIO
        protein = ProtIO.load("3i40.prot")[0]

        protein.set_attribute("note", "The file describes Human Insulin")
        protein.set_attribute("organism", "Homo Sapiens")
        protein.set_attribute("resolution", 1.85)
        protein.get_chain("A").set_attribute("name", "Insulin A chain")
        protein.get_chain("A").get_residue(0).set_attribute('first', True)

        print(protein.get_attribute("note"))
        print(protein.get_attribute("organism"))
        print(protein.get_attribute("resolution"))
        print(protein.get_chain("A").has_attribute("name"))
        print(protein.get_chain("A").get_attribute("name"))
        print(protein.get_chain("B").has_attribute("name"))
        print(protein.get_chain("A").get_residue(0).get_attribute('first'))

        ProtIO.save(protein, "3140_with_attributes.prot")
        protein = ProtIO.load("3140_with_attributes.prot")[0]
        print(protein.get_attribute("note"))

    @staticmethod
    def hydrophobicity():
        from src.file_io.prot_io import ProtIO
        from src.properties.hydrophobicity import Hydrophobicity

        protein = ProtIO.load("3i40.prot")[0]
        Hydrophobicity.add_hydrophobicity_to_protein(protein)

        print(protein.get_attribute("hydrophobicity"))
        print(protein.get_chain("A").get_attribute("hydrophobicity"))
        print(protein.get_chain("B").get_attribute("hydrophobicity"))
        print(protein.get_chain("A").get_residue(0).get_attribute("hydrophobicity"))

Examples.hydrophobicity()
# Examples.set_get_attribute()
# Examples.seqres_records()
# Examples.missing_or_extra_atoms()
# Examples.keep_backbone_atoms()
# Examples.remove_atoms()
# Examples.remove_hydrogen_atoms()
# Examples.fix_disordered_atoms()
# Examples.remove_heteroatoms()
# Examples.remove_water()
