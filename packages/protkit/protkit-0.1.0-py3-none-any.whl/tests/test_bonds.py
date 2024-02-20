import prepare_data


def test_bond_lengths():
    from protkit.properties.bond_lengths import BondLengths
    # Get a sample protein
    protein = prepare_data.sample_pdb()

    # Calculate the bond lengths
    bond_lengths = BondLengths.bond_lengths_of_protein(protein)
    assert (abs(bond_lengths['A']['ASP1'][('N', 'CA')] - 1.4576138034472625) < 0.00001)

    # Calculate bond lengths and assign
    BondLengths.bond_lengths_of_protein(protein, assign_attribute=True)
    assert (abs(protein.get_chain('A').get_residue(0).get_attribute('bond_lengths')[('N', 'CA')] - 1.4576138034472625) < 0.00001)

    BondLengths.peptide_bond_lengths_of_protein(protein, assign_attribute=True)
    assert (abs(protein.get_chain('A').get_attribute('peptide_bond_lengths')[0] - 1.350036295808375) < 0.00001)


def test_bond_angles():
    from protkit.properties.bond_angles import BondAngles
    # Get a sample protein
    protein = prepare_data.sample_pdb()

    # Calculate the bond angles
    bond_angles = BondAngles.bond_angles_of_protein(protein, assign_attribute=True)
    assert (abs(protein.get_chain('A').get_residue(0).get_attribute('bond_angles')[('OD1', 'CG', 'OD2')] - 123.15968284788724) < 0.00001)


def test_dihedral_angles():
    from protkit.properties.dihedral_angles import DihedralAngles
    # Get a sample protein
    protein = prepare_data.sample_pdb()

    # Calculate the dihedral angles
    dihedral_angles = DihedralAngles.dihedral_angles_of_protein(protein, assign_attribute=True)
    assert (abs(protein.get_chain('A').get_residue(1).get_attribute('dihedral_angles')['PHI'] - -100.537017489208) < 0.00001)


# xtest_bond_lengths()
# xtest_bond_angles()
# xtest_dihedral_angles()

