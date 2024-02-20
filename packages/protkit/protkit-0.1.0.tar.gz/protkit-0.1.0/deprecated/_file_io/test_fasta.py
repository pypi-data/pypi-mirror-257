from src.core.sequence import Sequence
from src.file_io.fasta_io import FastaIO

file_name_in = "src/test/1AHW.fasta"
file_name_out = "src/test/1AHW_out.fasta"

sequences = FastaIO.load(file_name_in)
for seq in sequences:
    print(seq.description)
    print(seq.sequence)
FastaIO.save(file_name_out, sequences)