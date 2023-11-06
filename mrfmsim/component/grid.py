#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from mrfmsim.component import ComponentBase
from dataclasses import dataclass, field


@dataclass
class Grid(ComponentBase):
    """Instantiate a rectangular grid with shape, step and origin.

    The resulting grid has equal spacing in each dimension.
    The grid array uses numpy's open mesh-grid, which has speed and storage
    benefits.

    :param np.array length: array of lengths along (x, y, z)
    :param np.array step: a list of step sizes
    :param np.array origin: the grid origin

    :param tuple[int] shape: grid dimension
        (number of points in x, y, z direction)
    :param list step: grid setup size in x, y, z direction
    :param list origin: grid origin
    :param float voxel: the volume of each grid voxel
    :param np.array range: range in (x, y, z direction), shape (3, 2)
    :param np.array length: actual lengths of the grid. This is recalculated
        based on the rounded value of grid shape and step size.
    """

    shape: tuple[int]
    step: list[float] = field(metadata={"unit": "nm"})
    origin: list[float] = field(metadata={"unit": "nm"})
    voxel: float = field(init=False, metadata={"unit": "nm^3"})
    range: np.array = field(init=False, metadata={"unit": "nm"})
    length: np.array = field(init=False, metadata={"unit": "nm"})

    def __post_init__(self):
        """Calculate grid parameters."""

        self.voxel = np.array(self.step).prod()
        self.range = (np.array(self.shape) - [1, 1, 1]) * self.step
        self.length = np.array(self.shape) * np.array(self.step)

    @staticmethod
    def grid_extents(length, origin):
        """Calculate grid extents based on the grid length and origin.

        The result is column stacked into a dimension of (3, 2)
        """

        return np.column_stack((-length / 2 + origin, length / 2 + origin))

    @property
    def grid_array(self):
        """Generate an open mesh-grid of the given grid dimensions.

        The benefit of the property is that it generates the grid array at run time.
        """

        extents = self.grid_extents(self.range, self.origin)

        return np.ogrid[
            extents[0][0] : extents[0][1] : self.shape[0] * 1j,
            extents[1][0] : extents[1][1] : self.shape[1] * 1j,
            extents[2][0] : extents[2][1] : self.shape[2] * 1j,
        ]

    def extend_grid_method(self, ext_pts):
        """Extend the grid by the number of points in the x, y, z direction (one side).

        :param int ext_pts: points to extend along x direction
            (cantilever motion direction).
        """

        ext_shape = np.array(
            [
                self.shape[0] + np.array(ext_pts) * 2,
                self.shape[1],
                self.shape[2],
            ]
        )
        ext_range = (ext_shape - [1, 1, 1]) * self.step
        extents = self.grid_extents(ext_range, self.origin)

        return np.ogrid[
            extents[0][0] : extents[0][1] : ext_shape[0] * 1j,
            extents[1][0] : extents[1][1] : ext_shape[1] * 1j,
            extents[2][0] : extents[2][1] : ext_shape[2] * 1j,
        ]
