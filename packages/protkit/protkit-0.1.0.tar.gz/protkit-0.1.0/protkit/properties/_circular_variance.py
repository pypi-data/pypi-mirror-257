from sklearn.neighbors import KDTree
import numpy as np
from typing import *

from protkit.structure.protein import Protein
from protkit.properties.property_setter import PropertySetter

class CircularVariance(PropertySetter):
    def __init__(self, radius: float = 1.0, assign_to_protein: bool = True):
        self._radius = radius
        self._assign_to_protein = assign_to_protein

    def calculate_atom_property(self, protein: Protein):
        atom_coordinates = [(atom.x, atom.y, atom.z) for atom in protein.atoms]
        atom_coordinates = np.array(atom_coordinates)
        atom_tree = KDTree(atom_coordinates, leaf_size=50)
        circular_variance_by_atom = []

        for atom in protein.atoms:
            # Get the coordinate associated with the atom
            atom_coordinate = [atom.x, atom.y, atom.z]

            # Determine distances and neighbours to all the neighbouring atoms.
            atom_coordinate = np.array([atom_coordinate])
            neighbours, distances = atom_tree.query_radius(atom_coordinate, r=self._radius, return_distance=True)
            neighbours = neighbours[0]
            distances = distances[0]

            # Calculate circular variance.
            non_zero_indices = np.where(distances > 0.01)
            neighbour_coordinates = atom_coordinates[neighbours[non_zero_indices]]
            unit_vectors = neighbour_coordinates - atom_coordinate
            unit_vectors /= distances[non_zero_indices].reshape(-1, 1)
            cv = 1.0 - np.linalg.norm(np.sum(unit_vectors, axis=0)) / neighbours[non_zero_indices].shape[0]

            # Assignment
            if self._assign_to_protein:
                atom.set_attribute("circular_variance_by_atom", float(cv))

            circular_variance_by_atom.append(float(cv))

        return circular_variance_by_atom

    # def calculate_residue_property(self, protein: Protein):
    #     atoms = protein.filter_atoms(atom_criteria=[('atom_type', 'CA')])
    #     residue_coordinates = [(atom.x, atom.y, atom.z) for atom in atoms]
    #     residue_coordinates = np.array(residue_coordinates)
    #     residue_tree = KDTree(residue_coordinates, leaf_size=50)
    #
    #     for chain in protein._chains.values():
    #         self._circular_variance_by_residue[chain._chain_id] = {}
    #         for residue in chain._residues:
    #             # Get the coordinate associated with the residue
    #             atom = residue._atoms["CA"]
    #             residue_coordinate = [atom.x, atom.y, atom.z]
    #
    #             if residue_coordinate is None:
    #                 self._circular_variance_by_residue[chain._chain_id][residue._sequence_no] = None
    #             else:
    #                 # Construct a KD tree from all the coordinates of all the residues in the protein.
    #                 if residue_tree is None:
    #                     residue_tree = KDTree(residue_coordinates, leaf_size=50)
    #
    #                 # Determine distances and neighbours to all the neighbouring residues.
    #                 residue_coordinate = np.array([residue_coordinate])
    #                 neighbours, distances = residue_tree.query_radius(residue_coordinate, r=self._radius, return_distance=True)
    #                 neighbours = neighbours[0]
    #                 distances = distances[0]
    #
    #                 # Calculate circular variance.
    #                 non_zero_indices = np.where(distances > 0.01)
    #                 neighbour_coordinates = residue_coordinates[neighbours[non_zero_indices]]
    #                 unit_vectors = neighbour_coordinates - residue_coordinate
    #                 unit_vectors /= distances[non_zero_indices].reshape(-1, 1)
    #                 cv = 1.0 - np.linalg.norm(np.sum(unit_vectors, axis=0)) / neighbours[non_zero_indices].shape[0]
    #
    #                 # Assignment
    #                 self._circular_variance_by_residue[chain._chain_id][residue._sequence_no] = float(cv)

    def calculate_residue_property(self, protein: Protein):
        atoms = protein.filter_atoms(atom_criteria=[('atom_type', 'CA')])
        residue_coordinates = [(atom.x, atom.y, atom.z) for atom in atoms]
        residue_coordinates = np.array(residue_coordinates)
        residue_tree = KDTree(residue_coordinates, leaf_size=50)
        circular_variance_by_residue = []

        for residue in protein.residues:
            # Get the coordinate associated with the residue
            atom = residue.get_atom('CA')
            residue_coordinate = [atom.x, atom.y, atom.z]

            # Determine distances and neighbours to all the neighbouring residues.
            residue_coordinate = np.array([residue_coordinate])
            neighbours, distances = residue_tree.query_radius(residue_coordinate, r=self._radius, return_distance=True)
            neighbours = neighbours[0]
            distances = distances[0]

            # Calculate circular variance.
            non_zero_indices = np.where(distances > 0.01)
            neighbour_coordinates = residue_coordinates[neighbours[non_zero_indices]]
            unit_vectors = neighbour_coordinates - residue_coordinate
            unit_vectors /= distances[non_zero_indices].reshape(-1, 1)
            cv = 1.0 - np.linalg.norm(np.sum(unit_vectors, axis=0)) / neighbours[non_zero_indices].shape[0]

            # Assignment
            if self._assign_to_protein:
                residue.set_attribute("circular_variance_by_residue", float(cv))

            circular_variance_by_residue.append(float(cv))

        return circular_variance_by_residue

    # @staticmethod
    # def add_residue_property(self, protein: Protein, circular_variance_by_residue: List[float]) -> Protein:
    #     protein.assign_list(list(protein.residues), self._circular_variance_by_residue, "circular_variance_by_residue")