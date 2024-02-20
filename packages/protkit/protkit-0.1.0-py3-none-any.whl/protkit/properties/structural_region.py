import numpy as np
from typing import *

from protkit.structure.protein import Protein
from protkit.properties.property_setter import PropertySetter
from protkit.enum.element_template import ElementTemplate
from protkit.enum.residue_template import ResidueTemplate
from protkit.properties.surface_area import SurfaceArea
from protkit.tools.freesasa_adaptor import FreeSASAAdaptor

class StructuralRegion():
    def __init__(self, surface_area_adaptor: SurfaceArea, assign_to_protein: bool = True):
        self._surface_area_adaptor = surface_area_adaptor
        self._assign_to_protein = assign_to_protein

        self._MAX_ASA_MILLER = {
            "ALA": 113.0,
            "ARG": 241.0,
            "ASN": 158.0,
            "ASP": 151.0,
            "CYS": 140.0,
            "GLN": 189.0,
            "GLU": 183.0,
            "GLY": 85.0,
            "HIS": 194.0,
            "ILE": 182.0,
            "LEU": 180.0,
            "LYS": 211.0,
            "MET": 204.0,
            "PHE": 218.0,
            "PRO": 143.0,
            "SER": 122.0,
            "THR": 146.0,
            "TRP": 259.0,
            "TYR": 229.0,
            "VAL": 160.0
        }
        self._MAX_ASA_MILLER_INDEX = np.array([113.0, 140.0, 151.0, 183.0, 218.0,
                                         85.0, 194.0, 182.0, 211.0, 180.0,
                                         204.0, 158.0, 143.0, 189.0, 241.0,
                                         122.0, 146.0, 160.0, 259.0, 229.0])

        # Protein structural regions as defined by Levy (2010)
        self._REGION_INTERIOR = 0
        self._REGION_SURFACE = 1
        self._REGION_SUPPORT = 2
        self._REGION_RIM = 3
        self._REGION_CORE = 4
        self._STRUCTURAL_REGION_THRESHOLD = 0.25

    def calculate_structural_region(self, protein: Protein, receptor_chains: List[str], ligand_chains: List[str]) -> Dict:
        receptor = protein.copy(keep_chain_ids=receptor_chains)
        ligand = protein.copy(keep_chain_ids=ligand_chains)
        num_receptor_atoms = receptor.num_atoms
        num_ligand_atoms = ligand.num_atoms

        surface_area_calculator = SurfaceArea(surface_area_adaptor=self._surface_area_adaptor)
        atom_bound_surface_area = surface_area_calculator.calculate_atom_property(protein)

        receptor_atom_bound_surface_area = atom_bound_surface_area[:num_receptor_atoms]
        ligand_atom_bound_surface_area = atom_bound_surface_area[num_receptor_atoms:num_receptor_atoms + num_ligand_atoms]

        receptor_atom_unbound_surface_area = surface_area_calculator.calculate_atom_property(receptor)
        ligand_atom_unbound_surface_area = surface_area_calculator.calculate_atom_property(ligand)

        protein.assign_list(list(receptor.atoms), receptor_atom_bound_surface_area, "bound_sasa")
        protein.assign_list(list(receptor.atoms), receptor_atom_unbound_surface_area, "unbound_sasa")
        protein.assign_list(list(ligand.atoms), ligand_atom_bound_surface_area, "bound_sasa")
        protein.assign_list(list(ligand.atoms), ligand_atom_unbound_surface_area, "unbound_sasa")

        receptor_residue_bound_surface_area = []
        receptor_residue_unbound_surface_area = []
        for residue in receptor.residues:
            residue.sum_attribute("bound_sasa")
            receptor_residue_bound_surface_area.append(residue.get_attribute("bound_sasa"))
            residue.sum_attribute("unbound_sasa")
            receptor_residue_unbound_surface_area.append(residue.get_attribute("unbound_sasa"))

        ligand_residue_bound_surface_area = []
        ligand_residue_unbound_surface_area = []
        for residue in ligand.residues:
            residue.sum_attribute("bound_sasa")
            ligand_residue_bound_surface_area.append(residue.get_attribute("bound_sasa"))
            residue.sum_attribute("unbound_sasa")
            ligand_residue_unbound_surface_area.append(residue.get_attribute("unbound_sasa"))

        receptor_residue_bound_surface_area = np.array(receptor_residue_bound_surface_area)
        receptor_residue_unbound_surface_area = np.array(receptor_residue_unbound_surface_area)
        receptor_residue_type_encoding = [ResidueTemplate.STANDARD_RESIDUES[residue.residue_type]["int"] for residue in
                                        receptor.residues]
        ligand_residue_bound_surface_area = np.array(ligand_residue_bound_surface_area)
        ligand_residue_unbound_surface_area = np.array(ligand_residue_unbound_surface_area)
        ligand_residue_type_encoding = [ResidueTemplate.STANDARD_RESIDUES[residue.residue_type]["int"]for residue in ligand.residues]

        receptor_structural_regions = self.structural_regions(receptor_residue_unbound_surface_area,
                                                              receptor_residue_bound_surface_area,
                                                              receptor_residue_type_encoding)
        ligand_structural_regions = self.structural_regions(ligand_residue_unbound_surface_area,
                                                            ligand_residue_bound_surface_area,
                                                            ligand_residue_type_encoding)

        if self._assign_to_protein:
            protein.assign_list(list(protein.filter_residues(chain_criteria=[('chain_id', receptor_chains)])), receptor_structural_regions, "structural_region")
            protein.assign_list(list(protein.filter_residues(chain_criteria=[('chain_id', ligand_chains)])), ligand_structural_regions, "structural_region")

        return receptor_structural_regions, ligand_structural_regions

    def calculate_structural_region2(self, protein: Protein, receptor_chains: List[str], ligand_chains: List[str]) -> Dict:
        receptor = protein.copy(keep_chain_ids=receptor_chains)
        ligand = protein.copy(keep_chain_ids=ligand_chains)
        num_receptor_atoms = receptor.num_atoms
        num_ligand_atoms = ligand.num_atoms

        surface_area_calculator = SurfaceArea(surface_area_adaptor=self._surface_area_adaptor)
        atom_bound_surface_area = surface_area_calculator.calculate_atom_property(protein)

        receptor_atom_bound_surface_area = atom_bound_surface_area[:num_receptor_atoms]
        ligand_atom_bound_surface_area = atom_bound_surface_area[
                                         num_receptor_atoms:num_receptor_atoms + num_ligand_atoms]

        receptor_atom_unbound_surface_area = surface_area_calculator.calculate_atom_property(receptor)
        ligand_atom_unbound_surface_area = surface_area_calculator.calculate_atom_property(ligand)

        receptor_residue_bound_surface_area = []
        receptor_residue_unbound_surface_area = []
        atom_counter = 0
        for residue in receptor.residues:
            receptor_residue_bound_surface_area.append(sum(receptor_atom_bound_surface_area[atom_counter:atom_counter + residue.num_atoms]))
            receptor_residue_unbound_surface_area.append(sum(receptor_atom_unbound_surface_area[atom_counter:atom_counter + residue.num_atoms]))
            atom_counter += residue.num_atoms

        ligand_residue_bound_surface_area = []
        ligand_residue_unbound_surface_area = []
        atom_counter = 0
        for residue in ligand.residues:
            ligand_residue_bound_surface_area.append(sum(ligand_atom_bound_surface_area[atom_counter:atom_counter + residue.num_atoms]))
            ligand_residue_unbound_surface_area.append(sum(ligand_atom_unbound_surface_area[atom_counter:atom_counter + residue.num_atoms]))
            atom_counter += residue.num_atoms

        receptor_residue_bound_surface_area = np.array(receptor_residue_bound_surface_area)
        receptor_residue_unbound_surface_area = np.array(receptor_residue_unbound_surface_area)
        receptor_residue_type_encoding = [ResidueTemplate.STANDARD_RESIDUES[residue.residue_type]["int"] for residue in
                                        receptor.residues]
        ligand_residue_bound_surface_area = np.array(ligand_residue_bound_surface_area)
        ligand_residue_unbound_surface_area = np.array(ligand_residue_unbound_surface_area)
        ligand_residue_type_encoding = [ResidueTemplate.STANDARD_RESIDUES[residue.residue_type]["int"]for residue in ligand.residues]

        receptor_structural_regions = self.structural_regions(receptor_residue_unbound_surface_area,
                                                              receptor_residue_bound_surface_area,
                                                              receptor_residue_type_encoding)
        ligand_structural_regions = self.structural_regions(ligand_residue_unbound_surface_area,
                                                            ligand_residue_bound_surface_area,
                                                            ligand_residue_type_encoding)


        if self._assign_to_protein:
            protein.assign_list(list(protein.filter_residues(chain_criteria=[('chain_id', receptor_chains)])), receptor_structural_regions, "structural_region")
            protein.assign_list(list(protein.filter_residues(chain_criteria=[('chain_id', ligand_chains)])), ligand_structural_regions, "structural_region")

        return receptor_structural_regions, ligand_structural_regions

    def structural_regions(self,
                           asa_monomer: np.ndarray,
                           asa_complex: np.ndarray,
                           residue_type: np.ndarray) -> np.ndarray:
        """
        Computes the structural region associated with each residue
        as described in the paper by Levy et al. (2010).

        The region can be one of:
        INTERIOR: Inside the protein, not exposed to the surface.
        SURFACE:  On the surface of the protein, but not part of the interface.
        SUPPORT:  Part of the interface site, buried below the core but above the interior.
        RIM:      Part of the interface site, but on the outer edge between surface and core.
        CORE:     The core part of the interface between two proteins.

        Args:
            asa_monomer: Accessible surface area in the unbound (monomer) state.
            asa_complex: Accessible surface area in the bound (complex) state.
            residue_type: Residue type encoded as an index.
            threshold: Threshold to use to distinguish between different structural regions.

        Returns:
            Array specifying the type of region associated with each residue.
        """

        # Calculate areas
        max_asa = self._MAX_ASA_MILLER_INDEX[residue_type]
        rasa_monomer = asa_monomer / max_asa
        rasa_complex = asa_complex / max_asa
        drasa = rasa_monomer - rasa_complex

        # Identify regions
        interior_idx = (drasa <= 0.0) & (rasa_complex < self._STRUCTURAL_REGION_THRESHOLD)
        surface_idx = (drasa <= 0.0) & (rasa_complex >= self._STRUCTURAL_REGION_THRESHOLD)
        support_idx = (drasa > 0.0) & (rasa_monomer < self._STRUCTURAL_REGION_THRESHOLD)
        rim_idx = (drasa > 0.0) & (rasa_complex >= self._STRUCTURAL_REGION_THRESHOLD)
        core_idx = (drasa > 0.0) & (rasa_monomer >= self._STRUCTURAL_REGION_THRESHOLD) & (rasa_complex < self._STRUCTURAL_REGION_THRESHOLD)

        # Construct region vector
        regions = np.zeros_like(residue_type, dtype=int)
        regions[interior_idx] = self._REGION_INTERIOR
        regions[surface_idx] = self._REGION_SURFACE
        regions[support_idx] = self._REGION_SUPPORT
        regions[rim_idx] = self._REGION_RIM
        regions[core_idx] = self._REGION_CORE

        return regions
