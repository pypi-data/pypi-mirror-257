#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@Authors:  Fred Senekal (FS)
@Contact:  fred@silicogenesis.com
@License:  GPLv3
@Date:     July 2022 - November 2023

The class provides an abstraction of a KD Tree.
"""

from sklearn.neighbors import KDTree
from protkit.structure.chain import Chain



class SpaceQuery:
    def __init__(self, coordinates: list, leaf_size: int = 50):
        """
        Constructor.

        Args:
            coordinates (list): A list of coordinates.
            leaf_size (int): The leaf size of the KD Tree.

        Returns:
            None

        Raises:
            None
        """
        self._coordinates = coordinates
        self._tree = KDTree(coordinates, leaf_size=leaf_size)

    def query_radius(self, coordinate: list, radius: float, return_distance: bool = False) -> tuple:
        """
        Queries the KD Tree for all points within a given radius of a given coordinate.

        Args:
            coordinate (list): The coordinate to query.
            radius (float): The radius to search within.

        Returns:
            tuple: The indices of the points within the radius and the distances of the points from the coordinate.

        Raises:
            None
        """
        return self._tree.query_radius(coordinate, r=radius, return_distance=return_distance)

    @staticmethod
    def from_chain(chain: Chain):
        """
        Constructs a KD Tree from the coordinates of the atoms in a chain.

        Args:
            chain (Chain): The chain.

        Returns:
            SpaceQuery: The KD Tree.

        Raises:
            None
        """
        coordinates = [(atom.x, atom.y, atom.z) for atom in chain.atoms]
        return SpaceQuery(coordinates)
