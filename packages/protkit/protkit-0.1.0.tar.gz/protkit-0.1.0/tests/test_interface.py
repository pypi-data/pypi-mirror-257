import prepare_data


def test_atom_interface():
    from protkit.properties.interface import Interface

    # Get a sample protein
    protein = prepare_data.sample_pdb()

    # Get the atoms of the first chain
    atoms1 = list(protein.get_chain('A').atoms)
    atoms2 = list(protein.get_chain('B').atoms)

    # Get the interface atoms
    interface_atoms1, interface_atoms2 = Interface.interface_atoms(atoms1, atoms2, cutoff=6.0)
    assert (len(interface_atoms1) == 305)
    assert (len(interface_atoms2) == 326)

    interface_atoms1, interface_atoms2 = Interface.interface_atoms(atoms1, atoms2, cutoff=5.0)
    assert (len(interface_atoms1) == 201)
    assert (len(interface_atoms2) == 227)

    interface_atoms1, interface_atoms2 = Interface.interface_atoms(atoms1, atoms2, cutoff=4.0)
    assert (len(interface_atoms1) == 103)
    assert (len(interface_atoms2) == 113)

    interface_atoms1, interface_atoms2 = Interface.interface_atoms(atoms1, atoms2, cutoff=1.0)
    assert (len(interface_atoms1) == 0)
    assert (len(interface_atoms2) == 0)

def test_residue_interface():
    from protkit.properties.interface import Interface

    # Get a sample protein
    protein = prepare_data.sample_pdb()

    # Get the residues of the first chain
    residues1 = list(protein.get_chain('A').residues)
    residues2 = list(protein.get_chain('B').residues)

    # Get the interface residues
    interface_residues1, interface_residues2 = Interface.interface_residues(residues1, residues2, cutoff=6.0, assign_attribute=True)
    assert (len(interface_residues1) == 59)
    assert (len(interface_residues2) == 60)

    interface_residues1, interface_residues2 = Interface.interface_residues(residues1, residues2, cutoff=5.0, assign_attribute=True)
    assert (len(interface_residues1) == 46)
    assert (len(interface_residues2) == 53)

    interface_residues1, interface_residues2 = Interface.interface_residues(residues1, residues2, cutoff=4.0, assign_attribute=True)
    assert (len(interface_residues1) == 36)
    assert (len(interface_residues2) == 35)

    interface_residues1, interface_residues2 = Interface.interface_residues(residues1, residues2, cutoff=0.0, assign_attribute=True)
    assert (len(interface_residues1) == 0)
    assert (len(interface_residues2) == 0)


def test_residue_interface_with_alpha_carbon():
    from protkit.properties.interface import Interface

    # Get a sample protein
    protein = prepare_data.sample_pdb()

    # Get the residues of the first chain
    residues1 = list(protein.get_chain('A').residues)
    residues2 = list(protein.get_chain('B').residues)

    # Get the interface residues
    interface_residues1, interface_residues2 = Interface.interface_residues_from_alpha_carbon(residues1, residues2, cutoff=6.0, assign_attribute=True)
    assert (len(interface_residues1) == 5)
    assert (len(interface_residues2) == 6)

    interface_residues1, interface_residues2 = Interface.interface_residues_from_alpha_carbon(residues1, residues2, cutoff=5.0, assign_attribute=True)
    assert (len(interface_residues1) == 0)
    assert (len(interface_residues2) == 0)


# xtest_atom_interface()
# xtest_residue_interface()
# xtest_residue_interface_with_alpha_carbon()
