import prepare_data


def test_hydrophobicity_for_structure():
    from protkit.properties.hydrophobicity import Hydrophobicity

    # Get a sample protein
    protein = prepare_data.sample_pdb()

    # Calculate the hydrophobicity
    hydrophobicity = Hydrophobicity.hydrophobicity_of_protein(protein, assign_attribute=True)
    assert abs(hydrophobicity - -624.2) < 0.0001


def test_hydrophobicity_for_sequence():
    from protkit.seq.protein_sequence import ProteinSequence
    from protkit.properties.hydrophobicity import Hydrophobicity

    # Get sample sequences
    sequences = prepare_data.sample_sequences()

    # Calculate the hydrophobicity
    total = 0
    for sequence in sequences:
        protein_sequence = ProteinSequence.from_sequence(sequence)
        protein_sequence.to_triple_letter()
        total += Hydrophobicity.hydrophobicity_of_sequence(sequence)
    assert abs(total - -334.6) < 0.0001
