import prepare_data


def test_surface_area():
    from protkit.properties.surface_area import SurfaceArea

    # Get a sample protein
    protein = prepare_data.sample_pdb()

    # Calculate the solvent accessible surface area
    SurfaceArea.surface_area_of_protein(protein, assign_attribute=True)
    assert (abs(protein.get_attribute("surface_area") - 55507.781515525196) < 0.0001)


test_surface_area()