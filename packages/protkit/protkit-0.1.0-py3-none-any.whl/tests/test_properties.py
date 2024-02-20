import prepare_data


def test_properties():
    from protkit.properties.properties import Properties

    # Get a sample protein
    protein = prepare_data.sample_pdb()

    Properties.assign_properties_of_protein(protein)

    print(f"Protein mass: {protein.get_attribute('mass')}")
    print(f"Protein volume: {protein.get_attribute('volume')}")
    print(f"Protein hydrophobicity: {protein.get_attribute('hydrophobicity')}")

