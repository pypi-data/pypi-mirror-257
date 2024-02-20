import subprocess

from protkit.structure.protein import Protein
from protkit.tasks.protonator import Protonator, ProtonationError, DeprotonationError
from protkit.file_io.pdb_io import PDBIO

class ReduceAdaptor(Protonator):
    """
    ReduceAdaptor is an implementation of the Protonator abstract class,
    providing functionality to protonate a protein using the Reduce tool.
    """

    def __init__(self, reduce_bin_path: str, build: bool = False):
        """Initializes the ReduceAdaptor instance."""
        super().__init__()
        self._reduce_bin_path = reduce_bin_path
        self._build = build

    @staticmethod
    def merge(protein1: Protein, protein2: Protein) -> Protein:
        """Updates protein1 with the information from protein2."""
        for chain in protein2.chains:
            for index, residue in enumerate(chain.residues):
                for atom in residue.atoms:
                    protein1_atom = protein1.get_chain(chain.chain_id).get_residue(index).get_atom(atom.atom_type)
                    if protein1_atom is None:
                        protein1.get_chain(chain.chain_id).get_residue(index).add_atom(atom.atom_type, atom)
                    else:
                        if protein1_atom.x != atom.x or protein1_atom.y != atom.y or protein1_atom.z != atom.z:
                            protein1_atom.x = atom.x
                            protein1_atom.y = atom.y
                            protein1_atom.z = atom.z

        return protein1



    def protonate(self, protein_in: Protein) -> Protein:
        """
        Protonates a protein using the Reduce tool.

        Parameters:
            protein (Protein): The protein to be protonated.

        Returns:
            Protein: The protonated protein.
        """
        # Create an in memory PDB file
        input_pdb_file = PDBIO.to_pdb_text(protein_in)


        # Remove protons first, in case the structure is already protonated
        deprotonate_process = subprocess.Popen([self._reduce_bin_path, "-Trim", "-"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        deprotonate_process.stdin.write(input_pdb_file.encode())
        stdout, stderr = deprotonate_process.communicate()
        deprotonate_process_output = stdout.decode("utf8")
        deprotonate_process.stdin.close()
        if deprotonate_process.stderr is not None:
            raise DeprotonationError(
                "Error while deprotonating the protein before protonation."
            )
        deprotonated_pdb = deprotonate_process_output

        if self._build:
            protonate_process = subprocess.Popen([self._reduce_bin_path, "-build", "-"], stdin=subprocess.PIPE,
                                                 stdout=subprocess.PIPE)
        else:
            protonate_process = subprocess.Popen([self._reduce_bin_path, "-HIS", "-"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        protonate_process.stdin.write(deprotonated_pdb.encode())
        stdout, stderr = protonate_process.communicate()
        protonate_process_out = stdout.decode("utf8")
        protonate_process.stdin.close()
        if protonate_process.stderr is not None:
            raise ProtonationError(
                "Error while protonating the protein."
            )
        protonated_pdb = protonate_process_out
        protein_out = PDBIO.from_pdb_text(protonated_pdb)[0]
        protein = ReduceAdaptor.merge(protein_in, protein_out)

        return protein
