import prepare_data


def xtest_circular_variance_by_atom():
    from protkit.properties.circular_variance import CircularVariance

    # Get a sample protein
    protein = prepare_data.sample_pdb()

    # Calculate the circular variance
    circular_variance = CircularVariance.circular_variance_by_atom(protein, radius=5.0, assign_attribute=True)
    # assert abs(circular_variance[0] - 0.0) < 0.0001

def xtest_circular_variance_by_residue():
    from protkit.properties.circular_variance import CircularVariance

    # Get a sample protein
    protein = prepare_data.sample_pdb()

    # Calculate the circular variance
    circular_variance = CircularVariance.circular_variance_by_residue(protein, radius=1.0, assign_attribute=True)
    # assert abs(circular_variance[0] - 0.0) < 0.0001

xtest_circular_variance_by_atom()