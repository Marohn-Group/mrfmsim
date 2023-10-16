#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


class Grid:
    """Instantiate a rectangular grid with length, step and origin.
    
    The resulting grid has equal spacing in each dimension.
    The grid array uses numpy's open mesh-grid, which has speed and storage
    benefits.
    """

    def __init__(self, shape, step, origin=[0, 0, 0]):
        """Construct the grid object.
    
        The grid's step sizes, lengths, and the number of points are fixed at
        instantiation time.  The grid's step sizes and lengths are thus
        *not* updated if you manually reset the ``L`` or ``dL`` elements of
        the object manually later.
        If the lengths (``L``, etc) is not an integer multiple of the step
        sizes (``dL``, etc), then use for the lengths the closest multiple of
        the step sizes. This rounding is done silently and no error is flagged.
        .. Note::
            The grid shape is forced to be odd in the x and y directions, to avoid
            artifact when convolve.
        :param np.array length: array of lengths along (x, y, z)
        :param np.array step: a list of step sizes
        :param np.array origin: the grid origin
        :ivar np.array grid_length: actual lengths of the grid. This is recalculated
            based on the rounded value of grid shape and step size.
        :ivar np.array grid_origin: grid origin
        :ivar np.array grid_step: grid setup size in x, y, z direction
        :ivar float v_voxel: the volume of each grid voxel
        :ivar tuple grid_shape: grid dimension
            (number of points in x, y, z direction)
        :ivar np.array _range: range in (x, y, z direction), shape (3, 2)
        :ivar np.array grid_array: the grid coordinates in x, y, z direction
        """

        self.grid_origin = np.array(origin, dtype=np.float64)
        self.grid_step = np.array(step, dtype=np.float64)
        self.grid_voxel = self.grid_step.prod()
        self.grid_shape = np.array(shape).astype(int)
        self.grid_range = (self.grid_shape - [1, 1, 1]) * self.grid_step
        self.grid_length = self.grid_shape * self.grid_step

    @staticmethod
    def grid_extents(length, origin):
        """Calculate grid extents based on the grid length and origin.

        The result is column stacked into a dimension of (3, 2)
        """

        return np.column_stack((-length / 2 + origin, length / 2 + origin))

    @property
    def grid_array(self):
        """Generate an open mesh-grid of the given grid dimensions.
    
        The benefit of the property is that it cannot be modified,
        therefore, it is not included when using ``vars()`` to obtain
        the object dictionary. It also generates at runtime.
        """

        extents = self.grid_extents(self.grid_range, self.grid_origin)

        return np.ogrid[
            extents[0][0] : extents[0][1] : self.grid_shape[0] * 1j,
            extents[1][0] : extents[1][1] : self.grid_shape[1] * 1j,
            extents[2][0] : extents[2][1] : self.grid_shape[2] * 1j,
        ]


    def extend_grid_method(self, ext_pts):
        """Extend the grid by the number of points in the x, y, z direction (one side).

        :param int ext_pts: points to extend along x direction
            (cantilever motion direction).
        """

        ext_shape = np.array([
            self.grid_shape[0] + np.array(ext_pts) * 2,
            self.grid_shape[1],
            self.grid_shape[2],
        ])
        ext_range = (ext_shape - [1, 1, 1]) * self.grid_step
        extents = self.grid_extents(ext_range, self.grid_origin)

        return np.ogrid[
            extents[0][0] : extents[0][1] : ext_shape[0] * 1j,
            extents[1][0] : extents[1][1] : ext_shape[1] * 1j,
            extents[2][0] : extents[2][1] : ext_shape[2] * 1j,
        ]
