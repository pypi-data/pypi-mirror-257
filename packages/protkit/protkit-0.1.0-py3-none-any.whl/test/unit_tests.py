import filecmp
import os

from src.io.PDBIO import PDBIO
from src.io.ProtIO import ProtIO

class TestSG:
    CREATE_REF = True

    @staticmethod
    def test_setup():
        """
        Create the directories for the test.
        """
        if not os.path.exists("data_in"):
            os.mkdir("data_in")
            if not os.path.exists("data_in/pdb"):
                os.mkdir("data_in/pdb")
            if not os.path.exists("data_in/prot"):
                os.mkdir("data_in/prot")
        if not os.path.exists("data_ref"):
            os.mkdir("data_ref")
            if not os.path.exists("data_in/pdb"):
                os.mkdir("data_in/pdb")
            if not os.path.exists("data_in/prot"):
                os.mkdir("data_out/prot")
        if not os.path.exists("data_out"):
            os.mkdir("data_out")
            if not os.path.exists("data_out/pdb"):
                os.mkdir("data_out/pdb")
            if not os.path.exists("data_out/prot"):
                os.mkdir("data_out/prot")

    @staticmethod
    def test_1():
        """
        Test the PDBIO class for loading and saving a PDB file.
        """
        file_name_in = "data_in/pdb/1ahw.pdb"
        file_name_out = "data_out/pdb/1ahw.pdb"
        file_name_ref = "data_ref/pdb/1ahw.pdb"

        protein = PDBIO.load(file_name_in)[0]
        PDBIO.save(protein, file_name_out)
        if TestSG.CREATE_REF:
            PDBIO.save(protein, file_name_ref)
        assert filecmp.cmp(file_name_out, file_name_ref, shallow=False)

    @staticmethod
    def test_2():
        """
        Test conversion from a PDB file to Prot file.
        """
        file_name_in = "data_in/pdb/1ahw.pdb"
        file_name_out = "data_out/prot/1ahw.prot"
        file_name_ref = "data_ref/prot/1ahw.prot"
        file_name_out2 = "data_out/prot/1ahw.zprot"
        file_name_ref2 = "data_ref/prot/1ahw.zprot"

        protein = PDBIO.load(file_name_in)[0]

        # Uncompressed save
        ProtIO.save(protein, file_name_out, compress=False)
        if TestSG.CREATE_REF:
            ProtIO.save(protein, file_name_ref, compress=False)
        assert filecmp.cmp(file_name_out, file_name_ref, shallow=False)

        # Uncompressed convert
        ProtIO.convert(file_name_in, file_name_out, compress=False)
        assert filecmp.cmp(file_name_out, file_name_ref, shallow=False)

        # Compressed save
        ProtIO.save(protein, file_name_out2, compress=True)
        if TestSG.CREATE_REF:
            ProtIO.save(protein, file_name_ref2, compress=True)
        assert filecmp.cmp(file_name_out2, file_name_ref2, shallow=False)

        # Compressed convert
        ProtIO.convert(file_name_in, file_name_out2, compress=True)
        assert filecmp.cmp(file_name_out2, file_name_ref2, shallow=False)

    @staticmethod
    def test_3():
        """
        Test extracting a chain from a PDB file.
        """
        file_name_in = "data_in/pdb/1ahw.pdb"
        file_name_out = "data_out/prot/1ahw_A.zprot"
        file_name_ref = "data_ref/prot/1ahw_A.zprot"
        file_name_out2 = "data_out/prot/1ahw_B.zprot"
        file_name_ref2 = "data_ref/prot/1ahw_B.zprot"

        protein = PDBIO.load(file_name_in)[0]
        protein.keep_chains(["A"])
        ProtIO.save(protein, file_name_out)
        if TestSG.CREATE_REF:
            ProtIO.save(protein, file_name_ref)
        assert filecmp.cmp(file_name_out, file_name_ref, shallow=False)

        protein = PDBIO.load(file_name_in)[0]
        protein.remove_chains(["A"])
        ProtIO.save(protein, file_name_out2)
        if TestSG.CREATE_REF:
            ProtIO.save(protein, file_name_ref2)
        assert filecmp.cmp(file_name_out2, file_name_ref2, shallow=False)

