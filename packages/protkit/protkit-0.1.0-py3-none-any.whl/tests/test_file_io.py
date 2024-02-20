import os
import filecmp

DATA_DIR = "data/"
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)


def xtest_pdb_file_io():
    from protkit.download import Download
    from protkit.file_io.pdb_io import PDBIO

    # Download a file
    pdb_id = "1AHW"
    file_path_in = DATA_DIR + "1AHW.pdb"
    Download.download_pdb_file_from_rcsb(pdb_id, DATA_DIR)
    assert os.path.exists(file_path_in)

    # Load and save the file
    protein = PDBIO.load(file_path_in)[0]
    file_path_out = DATA_DIR + "1AHW2.pdb"
    PDBIO.save(protein, DATA_DIR + "1AHW2.pdb")
    assert os.path.exists(file_path_out)

    os.remove(file_path_in)
    os.remove(file_path_out)


def xtest_prot_with_compression_file_io():
    from protkit.download import Download
    from protkit.file_io.prot_io import ProtIO

    # Download a file
    pdb_id = "1AHW"
    file_path_in = DATA_DIR + "1AHW.pdb"
    Download.download_pdb_file_from_rcsb(pdb_id, DATA_DIR)
    assert os.path.exists(file_path_in)

    # Convert to prot file
    file_path_out = DATA_DIR + "1AHW.prot"
    ProtIO.convert(file_path_in, file_path_out)
    assert os.path.exists(file_path_out)

    # Read and write prot file
    protein = ProtIO.load(file_path_out)[0]
    file_path_out2 = DATA_DIR + "1AHW2.prot"
    ProtIO.save(protein, file_path_out2)
    assert os.path.exists(file_path_out2)

    # Ensure the files are the same
    assert filecmp.cmp(file_path_out, file_path_out2, shallow=False)

    os.remove(file_path_in)
    os.remove(file_path_out)
    os.remove(file_path_out2)


def xtest_prot_without_compression_file_io():
    from protkit.download import Download
    from protkit.file_io.prot_io import ProtIO

    # Download a file
    pdb_id = "1AHW"
    file_path_in = DATA_DIR + "1AHW.pdb"
    Download.download_pdb_file_from_rcsb(pdb_id, DATA_DIR)
    assert os.path.exists(file_path_in)

    # Convert to prot file
    file_path_out = DATA_DIR + "1AHWnc.prot"
    ProtIO.convert(file_path_in, file_path_out, compress=False)
    assert os.path.exists(file_path_out)

    # Read and write prot file
    protein = ProtIO.load(file_path_out, decompress=False)[0]
    file_path_out2 = DATA_DIR + "1AHW2nc.prot"
    ProtIO.save(protein, file_path_out2, compress=False)
    assert os.path.exists(file_path_out2)

    # Ensure the files are the same
    assert filecmp.cmp(file_path_out, file_path_out2, shallow=False)

    os.remove(file_path_in)
    os.remove(file_path_out)
    os.remove(file_path_out2)


def test_mmcif_file_io():
    pass


def test_mmtf_file_io():
    pass


def test_pqr_file_io():
    pass




