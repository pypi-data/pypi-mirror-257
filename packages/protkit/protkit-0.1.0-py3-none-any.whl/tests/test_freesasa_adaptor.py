import prepare_data


def test_freesasa_adaptor():
    from protkit.tools.freesasa_adaptor import FreeSASAAdaptor

    # Get a sample protein
    protein = prepare_data.sample_pdb()

    # Calculate the solvent accessible surface area using Lee Richards
    freesasa_adaptor = FreeSASAAdaptor(algorithm=FreeSASAAdaptor.LEE_RICHARDS)
    sasa = freesasa_adaptor.calculate_surface_area(list(protein.atoms))
    total_sasa = sum(sasa)
    assert (abs(total_sasa - 55507.781515525196) < 0.0001)

    # Calculate the solvent accessible surface area using Shrake Rupley
    freesasa_adaptor = FreeSASAAdaptor(algorithm=FreeSASAAdaptor.SHRAKE_RUPLEY)
    sasa = freesasa_adaptor.calculate_surface_area(list(protein.atoms))
    total_sasa = sum(sasa)
    assert (abs(total_sasa - 55556.27148127397) < 0.0001)


test_freesasa_adaptor()