import os

DATA_DIR = "data/"
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)


def xtest_sequence():
    from protkit.download import Download
    from protkit.file_io.fasta_io import FastaIO
    from protkit.seq.protein_sequence import ProteinSequence

    # Test by specifying the file path explicitly.
    pdb_id = "1AHW"
    file_path = DATA_DIR + "1AHW.fasta"
    # Download.download_fasta_file_from_rcsb(pdb_id, file_path)
    # assert os.path.exists(file_path)

    # Open the file and check the contents
    sequences = FastaIO.load(file_path)
    for i, sequence in enumerate(sequences):
        sequence = ProteinSequence.from_sequence(sequence)
        sequence.to_triple_letter()
        print(sequence)
        sequence.to_single_letter()
        print(sequence)
        sequence.set_attribute("no", i)
        print(sequence.get_attribute("no"))
        print(sequence.list_attributes())
        # print(sequence.description)

    # os.remove(file_path)

xtest_sequence()

