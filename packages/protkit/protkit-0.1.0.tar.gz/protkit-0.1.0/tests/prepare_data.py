"""
Prepares data for testing
"""

import os
from typing import List

from protkit.structure.protein import Protein
from protkit.seq.sequence import Sequence
from protkit.file_io.pdb_io import PDBIO
from protkit.file_io.fasta_io import FastaIO
from protkit.download import Download

DATA_DIR = "data/"
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)


def sample_pdb() -> Protein:
    pdb_id = "1AHW"
    file_path = os.path.join(DATA_DIR, pdb_id + ".pdb")
    if not os.path.exists(file_path):
        Download.download_pdb_file_from_rcsb(pdb_id, DATA_DIR)
        assert os.path.exists(file_path)

    return PDBIO.load(file_path)[0]


def sample_sequences() -> List[Sequence]:
    pdb_id = "1AHW"
    file_path = os.path.join(DATA_DIR, pdb_id + ".fasta")
    if not os.path.exists(file_path):
        Download.download_fasta_file_from_rcsb(pdb_id, DATA_DIR)
        assert os.path.exists(file_path)

    return FastaIO.load(file_path)