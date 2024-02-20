import os

DATA_DIR = "data/"
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)


def xtest_download():
    from protkit.download import Download
    url = "https://files.rcsb.org/download/3I40.pdb"
    file_path = DATA_DIR + "3I40.pdb"
    Download.download_file(url, file_path)
    assert os.path.exists(file_path)
    os.remove(file_path)


def xtest_parallel_download():
    from protkit.download import Download
    urls = ["https://files.rcsb.org/download/3I40.pdb",
            "https://files.rcsb.org/download/1AHW.pdb",
            "https://files.rcsb.org/download/1A8O.pdb"]
    file_paths = [DATA_DIR + "3I40.pdb",
                  DATA_DIR + "1AHW.pdb",
                  DATA_DIR + "1A8O.pdb"]
    Download.parallel_download(urls, file_paths, n_jobs=-1)
    for file_path in file_paths:
        assert os.path.exists(file_path)
        os.remove(file_path)


def xtest_download_pdb_from_rcsb():
    from protkit.download import Download

    # Test by specifying the file path explicitly.
    pdb_id = "3I40"
    file_path = DATA_DIR + "3I40.pdb"
    Download.download_pdb_file_from_rcsb(pdb_id, file_path)
    assert os.path.exists(file_path)
    os.remove(file_path)

    # Test by specifying the directory path.
    pdb_id = "1AHW"
    file_path = DATA_DIR + "1AHW.pdb"
    Download.download_pdb_file_from_rcsb(pdb_id, DATA_DIR)
    assert os.path.exists(file_path)
    os.remove(file_path)

    # Download multiple PDB files
    pdb_ids = ["3I40", "1AHW", "1A8O"]
    Download.download_pdb_files_from_rcsb(pdb_ids, DATA_DIR)
    for pdb_id in pdb_ids:
        file_path = DATA_DIR + f"{pdb_id}.pdb"
        assert os.path.exists(file_path)
        os.remove(file_path)


def xtest_download_cif_from_rcsb():
    from protkit.download import Download

    # Test by specifying the file path explicitly.
    pdb_id = "3I40"
    file_path = DATA_DIR + "3I40.cif"
    Download.download_cif_file_from_rcsb(pdb_id, file_path)
    assert os.path.exists(file_path)
    os.remove(file_path)

    # Test by specifying the directory path.
    pdb_id = "1AHW"
    file_path = DATA_DIR + "1AHW.cif"
    Download.download_cif_file_from_rcsb(pdb_id, DATA_DIR)
    assert os.path.exists(file_path)
    os.remove(file_path)

    # Download multiple PDB files
    pdb_ids = ["3I40", "1AHW", "1A8O"]
    Download.download_cif_files_from_rcsb(pdb_ids, DATA_DIR)
    for pdb_id in pdb_ids:
        file_path = DATA_DIR + f"{pdb_id}.cif"
        assert os.path.exists(file_path)
        os.remove(file_path)


def test_download_binary_cif_from_rcsb():
    from protkit.download import Download

    # Test by specifying the file path explicitly.
    pdb_id = "3I40"
    file_path = DATA_DIR + "3I40.bcif"
    Download.download_binary_cif_file_from_rcsb(pdb_id, file_path)
    assert os.path.exists(file_path)
    os.remove(file_path)

    # Test by specifying the directory path.
    pdb_id = "1AHW"
    file_path = DATA_DIR + "1AHW.bcif"
    Download.download_binary_cif_file_from_rcsb(pdb_id, DATA_DIR)
    assert os.path.exists(file_path)
    os.remove(file_path)

    # Download multiple PDB files
    pdb_ids = ["3I40", "1AHW", "1A8O"]
    Download.download_binary_cif_files_from_rcsb(pdb_ids, DATA_DIR)
    for pdb_id in pdb_ids:
        file_path = DATA_DIR + f"{pdb_id}.bcif"
        assert os.path.exists(file_path)
        os.remove(file_path)


def xtest_download_pdb_from_sabdab():
    from protkit.download import Download

    # Test by specifying the file path explicitly.
    pdb_id = "8AHN"
    file_path = DATA_DIR + "8AHN.pdb"
    Download.download_pdb_file_from_sabdab(pdb_id, file_path)
    assert os.path.exists(file_path)
    os.remove(file_path)

    # Test by specifying the directory path.
    pdb_id = "1AHW"
    file_path = DATA_DIR + "1AHW.pdb"
    Download.download_pdb_file_from_sabdab(pdb_id, DATA_DIR)
    assert os.path.exists(file_path)
    os.remove(file_path)

    # Download multiple PDB files
    pdb_ids = ["8AHN", "1AHW", "1KIQ"]
    Download.download_pdb_files_from_sabdab(pdb_ids, DATA_DIR)
    for pdb_id in pdb_ids:
        file_path = DATA_DIR + f"{pdb_id}.pdb"
        assert os.path.exists(file_path)
        os.remove(file_path)


def xtest_download_fasta_from_rcsb():
    from protkit.download import Download

    # Test by specifying the file path explicitly.
    pdb_id = "3I40"
    file_path = DATA_DIR + "3I40.fasta"
    Download.download_fasta_file_from_rcsb(pdb_id, file_path)
    assert os.path.exists(file_path)
    os.remove(file_path)

    # Test by specifying the directory path.
    pdb_id = "1AHW"
    file_path = DATA_DIR + "1AHW.fasta"
    Download.download_fasta_file_from_rcsb(pdb_id, DATA_DIR)
    assert os.path.exists(file_path)
    os.remove(file_path)

    # Download multiple FASTA files
    pdb_ids = ["3I40", "1AHW", "1A8O"]
    Download.download_fasta_files_from_rcsb(pdb_ids, DATA_DIR)
    for pdb_id in pdb_ids:
        file_path = DATA_DIR + f"{pdb_id}.fasta"
        assert os.path.exists(file_path)
        os.remove(file_path)


def xtest_download_fasta_from_uniprot():
    from protkit.download import Download

    # Test by specifying the file path explicitly.
    uniprot_id = "P0A6X3"
    file_path = DATA_DIR + "P0A6X3.fasta"
    Download.download_fasta_file_from_uniprot(uniprot_id, file_path)
    assert os.path.exists(file_path)
    os.remove(file_path)

    # Test by specifying the directory path.
    uniprot_id = "P0A6X4"
    file_path = DATA_DIR + ("P0A6X4.fasta")
    Download.download_fasta_file_from_uniprot(uniprot_id, DATA_DIR)
    assert os.path.exists(file_path)
    os.remove(file_path)

    # Download multiple FASTA files
    uniprot_ids = ["P0A6X3", "P0A6X4", "P0A6X5"]
    Download.download_fasta_files_from_uniprot(uniprot_ids, DATA_DIR, n_jobs=-1)
    for uniprot_id in uniprot_ids:
        file_path = DATA_DIR + f"{uniprot_id}.fasta"
        assert os.path.exists(file_path)
        os.remove(file_path)
