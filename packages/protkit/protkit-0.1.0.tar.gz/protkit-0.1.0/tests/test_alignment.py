# TODO: Comprehensive tests for alignment are needed

def test_global_alignment():
    from protkit.seq import Sequence, SequenceAlignment

    # Create sequences
    sequence1 = Sequence("ACGT")
    sequence2 = Sequence("ACG")

    # Align the sequences
    aligned1, aligned2 = SequenceAlignment.global_align(sequence1, sequence2)

    # Check the alignment
    assert "".join(aligned1) == "ACGT"
    assert "".join(aligned2) == "ACG-"

    # Align the sequences with a gap penalty
    aligned1, aligned2 = SequenceAlignment.global_align(sequence1, sequence2, gap_penalty=-2)

    # Check the alignment
    assert "".join(aligned1) == "ACGT"
    assert "".join(aligned2) == "ACG-"

    # Align the sequences with a mismatch penalty
    aligned1, aligned2 = SequenceAlignment.global_align(sequence1, sequence2, mismatch_penalty=-2)

    # Check the alignment
    assert "".join(aligned1) == "ACGT"
    assert "".join(aligned2) == "ACG-"

    # Align the sequences with a match value
    aligned1, aligned2 = SequenceAlignment.global_align(sequence1, sequence2, match_value=2)

    # Check the alignment
    assert "".join(aligned1) == "ACGT"
    assert "".join(aligned2) == "ACG-"


def test_local_alignment():
    from protkit.seq import Sequence, SequenceAlignment

    # Create sequences
    sequence1 = Sequence("ACGT")
    sequence2 = Sequence("ACG")

    # Align the sequences
    aligned1, aligned2 = SequenceAlignment.local_align(sequence1, sequence2)

    # Check the alignment
    assert "".join(aligned1) == "ACG"
    assert "".join(aligned2) == "ACG"

    # Align the sequences with a gap penalty
    aligned1, aligned2 = SequenceAlignment.local_align(sequence1, sequence2, gap_penalty=-2)

    # Check the alignment
    assert "".join(aligned1) == "ACG"
    assert "".join(aligned2) == "ACG"

    # Align the sequences with a mismatch penalty
    aligned1, aligned2 = SequenceAlignment.local_align(sequence1, sequence2, mismatch_penalty=-2)

    # Check the alignment
    assert "".join(aligned1) == "ACG"
    assert "".join(aligned2) == "ACG"

    # Align the sequences with a match value
    aligned1, aligned2 = SequenceAlignment.local_align(sequence1, sequence2, match_value=2)

    # Check the alignment
    assert "".join(aligned1) == "ACG"
    assert "".join(aligned2) == "ACG"
