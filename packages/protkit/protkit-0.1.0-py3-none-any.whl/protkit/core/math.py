#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@Authors:  Fred Senekal (FS)
@Contact:  fred@silicogenesis.com
@License:  GPLv3
@Date:     July 2022 - November 2023

The class provides common mathematical functions.
"""

from math import sqrt, pow
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from protkit.structure.atom import Atom


class Math:
    @staticmethod
    def distance(x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> float:
        """
        Calculates the Euclidean distance between two points.

        Args:
            x1 (float): The x-coordinate of the first point.
            y1 (float): The y-coordinate of the first point.
            z1 (float): The z-coordinate of the first point.
            x2 (float): The x-coordinate of the second point.
            y2 (float): The y-coordinate of the second point.
            z2 (float): The z-coordinate of the second point.

        Returns:
            float: The distance between the two points.

        Raises:
            None
        """
        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2
        return sqrt(dx * dx + dy * dy + dz * dz)


    @staticmethod
    def atom_distance(atom1: 'Atom', atom2: 'Atom') -> float:
        """
        Calculates the Euclidean distance between two atoms.

        Args:
            atom1 (Atom): The first atom.
            atom2 (Atom): The second atom.

        Returns:
            float: The distance between the two atoms.

        Raises:
            None
        """
        return Math.distance(atom1.x, atom1.y, atom1.z, atom2.x, atom2.y, atom2.z)
