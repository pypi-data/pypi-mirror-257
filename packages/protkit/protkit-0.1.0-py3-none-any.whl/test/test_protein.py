import pytest
from src.io.ProtIO import ProtIO
from src.io.PDBIO import PDBIO
from get_project_root import root_path


# >> "C:/Users/person/source/some_project/"

# @pytest.fixture(scope="module")
@pytest.fixture
def protein():
    project_root = root_path(ignore_cwd=True)
    prot_file = project_root + "\\test\\data_in\\pdb\\3i40.prot"
    prot = ProtIO.load(prot_file)[0]
    prot.pdb_id = "3i40"
    prot.remove_hetero_residues()
    # prot.set_attribute("Notes","Heteros!!!")
    return prot


@pytest.fixture
def raw_protein():
    project_root = root_path(ignore_cwd=True)
    prot_file = project_root + "\\test\\data_in\\pdb\\3i40.prot"
    raw_prot = ProtIO.load(prot_file)[0]
    return raw_prot


def test_copy(protein):
    copied_protein = protein.copy()
    assert copied_protein != protein
    assert copied_protein._pdb_id == protein._pdb_id
    copied_protein_a = protein.copy(keep_chain_ids="A")
    assert copied_protein_a.chain_ids == list("A")
    copied_protein_b = protein.copy(remove_chain_ids="A")
    assert copied_protein_b.chain_ids == list("B")


def test_create_chain(protein):
    protein.create_chain("C")
    assert "C" in protein._chains

    with pytest.raises(Exception) as excinfo:
        protein.create_chain("A")
    assert str(excinfo.value) == "Chain A already exists"


def test_add_chain(protein):
    chain = protein.get_chain("A")
    protein.add_chain("C", chain)
    assert "C" in protein._chains
    assert protein._chains["C"] == chain

    with pytest.raises(Exception) as excinfo:
        protein.add_chain("A", chain)
    assert str(excinfo.value) == "Chain A already exists"


def test_num_chains(protein):
    assert protein.num_chains == 2


def test_has_chain(protein):
    assert protein.has_chain("A") is True
    assert protein.has_chain("C") is False


def test_get_chain(protein):
    assert protein.get_chain("A").num_residues == 21
    assert protein.get_chain("C") is None


def test_filter_chains(protein):

    chains = protein.filter_chains(chain_criteria=[("chain_id", "A")])
    chains_str = ''.join(c.chain_id for c in chains)
    assert chains_str == "A"


def test_keep_chains(protein):
    protein.keep_chains(["B"])
    assert list(protein._chains.keys()) == ["B"]


def test_rename_chain(protein):

    protein.rename_chain("B", "D")
    assert "D" in protein._chains
    assert "B" not in protein._chains

    with pytest.raises(Exception) as excinfo:
        protein.rename_chain("G", "F")
    assert str(excinfo.value) == "Chain G does not exist"

    with pytest.raises(Exception) as excinfo:
        protein.rename_chain("D", "A")
    assert str(excinfo.value) == "Chain A already exists"


def test_remove_chains(protein):
    protein.remove_chains("A")
    assert "A" not in protein._chains

    with pytest.raises(Exception) as excinfo:
        protein.remove_chains(["B", "F"])
    assert str(excinfo.value) == "Chain F does not exist"


def test_get_set_attribute(protein):
    protein.set_attribute("test_attr", 123)
    assert protein.get_attribute("test_attr") == 123


def test_residues(protein):
    residues_str = ''.join(e.short_code for e in protein.residues)
    assert residues_str == 'GIVEQCCTSICSLYQLENYCNFVNQHLCGSHLVEALYLVCGERGFFYTPKA'


def test_num_residues(protein):
    assert protein.num_residues == 51


def test_num_disordered_residues(raw_protein):
    assert raw_protein.num_disordered_residues == 1


def test_num_hetero_residues(raw_protein):
    assert raw_protein.num_hetero_residues == 35


def test_num_residues_by_type(protein):
    assert protein.num_residues_by_type['LEU'] == 6


def test_filter_residues(protein):

    residues = protein.filter_residues(
        chain_criteria=[("chain_id", "A")],
        residue_criteria=[("residue_type", ["GLY", "SER"])]
    )
    residues_str = ''.join(r.short_code for r in residues)
    assert residues_str == "GSS"


def test_num_atoms(protein):
    assert protein.num_atoms == 403


def test_num_disordered_atoms(raw_protein):
    assert raw_protein.num_disordered_atoms == 8


def test_num_hetero_atoms(raw_protein):
    assert raw_protein.num_hetero_atoms == 35


def test_fix_disordered_atoms(raw_protein):
    assert raw_protein.num_disordered_atoms == 8
    raw_protein.fix_disordered_atoms()
    assert raw_protein.num_disordered_atoms == 0


def test_filter_atoms(protein):

    atoms = protein.filter_atoms(
        chain_criteria=[("chain_id", "A")],
        residue_criteria=[("residue_type", ["CYS", "SER"])],
        atom_criteria=[("element", ["S"])]
    )
    atoms_str = ''.join(a.element for a in atoms)
    assert atoms_str == "SSSS"


def test_remove_hydrogen_atoms(raw_protein):

    # TODO Add hydrogen atoms to remove them

    raw_protein.remove_hydrogen_atoms()
    atoms = raw_protein.filter_atoms(atom_criteria=[("element", ["H"])])
    atoms_str = ''.join(a.element for a in atoms)
    assert atoms_str == ''


def test_sum_attribute(protein):

    protein.sum_attribute("x")
    attr_val = protein.get_attribute("x")
    assert '{:.2f}'.format(attr_val) == '-7646.89'
